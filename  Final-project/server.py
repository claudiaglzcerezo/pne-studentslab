import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import re

PORT = 8080


# --- DATA FETCHING HELPERS ---
def fetch_ensembl(endpoint):
    url = f"https://rest.ensembl.org{endpoint}"
    req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return None


def get_gene_id(gene_name):
    data = fetch_ensembl(f"/lookup/symbol/homo_sapiens/{gene_name}")
    if data and "id" in data:
        return data["id"]
    return None


# #ADVANCED LEVEL
def send_clean_response(handler, title, html_content, raw_data, want_json):
    if want_json:
        handler.send_response(200)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(bytes(json.dumps(raw_data, indent=4), "utf-8"))
    else:
        html = f"""<!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>{title}</title></head>
        <body style="font-family: Arial, sans-serif; padding: 20px; background-color: lightgreen;">
            <h2 style="color: teal;">{title}</h2>
            <div style="background: white; padding: 20px; border-radius: 5px;">
                {html_content}
            </div>
            <br><a href="/">&larr; Back to Menu</a>
        </body>
        </html>"""
        handler.send_response(200)
        handler.send_header("Content-Type", "text/html")
        handler.end_headers()
        handler.wfile.write(bytes(html, "utf-8"))


# --- MAIN REQUEST HANDLER ---
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        params = urllib.parse.parse_qs(parsed_url.query)

        want_json = params.get("json", [None])[0] == "1"

        if path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open("index.html", "r", encoding="utf-8") as f:
                self.wfile.write(bytes(f.read(), "utf-8"))

        # #BASIC LEVEL
        elif path == "/listSpecies":
            limit = params.get("limit", [None])[0]
            data = fetch_ensembl("/info/species")
            if data and "species" in data:
                species_list = data["species"]
                if limit:
                    species_list = species_list[:int(limit)]

                html_out = "<ul>"
                for s in species_list:
                    html_out += f"<li>{s.get('display_name')} (<i>{s.get('name')}</i>)</li>"
                html_out += "</ul>"

                send_clean_response(self, "List of Species", html_out, species_list, want_json)
            else:
                send_clean_response(self, "Error", "Failed to get data.", {"error": "No data"}, want_json)

        elif path == "/karyotype":
            species = params.get("species", [None])[0]
            data = fetch_ensembl(f"/info/assembly/{species}")
            if data and "karyotype" in data:
                html_out = f"<p>Chromosomes for {species}:</p><ul>"
                for chrom in data["karyotype"]:
                    html_out += f"<li>Chromosome {chrom}</li>"
                html_out += "</ul>"

                send_clean_response(self, "Karyotype Info", html_out, data["karyotype"], want_json)
            else:
                send_clean_response(self, "Error", "Species not found.", {"error": "Not found"}, want_json)

        elif path == "/chromosomeLength":
            species = params.get("species", [None])[0]
            chromo = params.get("chromo", [None])[0]
            data = fetch_ensembl(f"/info/assembly/{species}")
            if data and "top_level_region" in data:
                length = None
                for region in data["top_level_region"]:
                    if str(region.get("name")).lower() == str(chromo).lower():
                        length = region.get("length")
                        break
                if length:
                    html_out = f"The length of the chromosome {chromo}: {length}"
                    json_out = {"species": species, "chromosome": chromo, "length": length}
                    send_clean_response(self, "Chromosome Length", html_out, json_out, want_json)
                else:
                    send_clean_response(self, "Error", "Chromosome not found.", {"error": "Not found"}, want_json)
            else:
                send_clean_response(self, "Error", "Species error.", {"error": "Server error"}, want_json)

        # #MEDIUM LEVEL
        elif path == "/geneLookup":
            gene = params.get("gene", [None])[0]
            stable_id = get_gene_id(gene)
            if stable_id:
                html_out = f"The stable ID for gene <b>{gene}</b> is: <b>{stable_id}</b>"
                json_out = {"gene": gene, "stable_id": stable_id}
                send_clean_response(self, "Gene Lookup", html_out, json_out, want_json)
            else:
                send_clean_response(self, "Error", "Gene not found.", {"error": "Not found"}, want_json)

        elif path == "/geneSeq":
            gene = params.get("gene", [None])[0]
            stable_id = get_gene_id(gene)
            if stable_id:
                seq_data = fetch_ensembl(f"/sequence/id/{stable_id}")
                if seq_data and "seq" in seq_data:
                    sequence = seq_data["seq"]
                    html_out = f"<p>Sequence:</p><textarea style='width:100%;height:150px;' readonly>{sequence}</textarea>"
                    json_out = {"gene": gene, "stable_id": stable_id, "sequence": sequence}
                    send_clean_response(self, "Gene Sequence", html_out, json_out, want_json)
                else:
                    send_clean_response(self, "Error", "Sequence error.", {"error": "Seq error"}, want_json)
            else:
                send_clean_response(self, "Error", "Gene not found.", {"error": "Not found"}, want_json)

        elif path == "/geneCalc":
            gene = params.get("gene", [None])[0]
            stable_id = get_gene_id(gene)
            if stable_id:
                seq_data = fetch_ensembl(f"/sequence/id/{stable_id}")
                if seq_data and "seq" in seq_data:
                    clean_seq = re.sub(r'\s+', '', seq_data["seq"]).upper()
                    total = len(clean_seq)
                    if total > 0:
                        p_a = round((clean_seq.count("A") / total) * 100, 2)
                        p_c = round((clean_seq.count("C") / total) * 100, 2)
                        p_g = round((clean_seq.count("G") / total) * 100, 2)
                        p_t = round((clean_seq.count("T") / total) * 100, 2)

                        html_out = f"<ul><li><b>Total Length:</b> {total} bp</li><li><b>A:</b> {p_a}% | <b>C:</b> {p_c}% | <b>G:</b> {p_g}% | <b>T:</b> {p_t}%</li></ul>"
                        json_out = {"gene": gene, "length": total,
                                    "percentages": {"A": p_a, "C": p_c, "G": p_g, "T": p_t}}
                        send_clean_response(self, "Gene Calculations", html_out, json_out, want_json)
                    else:
                        send_clean_response(self, "Error", "Empty sequence.", {"error": "Empty"}, want_json)
                else:
                    send_clean_response(self, "Error", "Sequence API error.", {"error": "API error"}, want_json)
            else:
                send_clean_response(self, "Error", "Gene not found.", {"error": "Not found"}, want_json)

        elif path == "/geneList":
            chrom = params.get("chromo", [None])[0]
            start = params.get("start", [None])[0]
            end = params.get("end", [None])[0]

            data = fetch_ensembl(f"/overlap/region/homo_sapiens/{chrom}:{start}-{end}?feature=gene")
            if isinstance(data, list):
                html_out = "<ul>"
                for item in data:
                    name = item.get("external_name", "Unknown")
                    html_out += f"<li><b>{name}</b> (ID: {item.get('id')})</li>"
                html_out += "</ul>"
                send_clean_response(self, "Overlapping Genes", html_out, data, want_json)
            else:
                send_clean_response(self, "Error", "Region fetch error.", {"error": "Region error"}, want_json)

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<h1>Error 404: Endpoint Not Found</h1>", "utf-8"))


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
        print(f"Server online on port {PORT}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")