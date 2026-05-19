import http.client
import http.server
import json
import socketserver
import urllib.parse

PORT = 8080
SERVER = "rest.ensembl.org"
PARAMS = "?content-type=application/json"


class TestHandler(http.server.BaseHTTPRequestHandler):

    def get_id(self, arguments):
        try:
            gene_symbol = arguments["gene"][0]
            ENDPOINT = f"/lookup/symbol/homo_sapiens/{gene_symbol}"
            conn = http.client.HTTPSConnection(SERVER)
            conn.request(
                "GET", ENDPOINT + PARAMS, headers={"Content-Type": "application/json"}
            )
            response = conn.getresponse()
            d = json.loads(response.read().decode())
            conn.close()
            return d.get("id")
        except Exception:
            return None

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        arguments = urllib.parse.parse_qs(parsed_url.query)
        is_json = "json" in arguments

        if path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            try:
                with open("index.html", "r", encoding="utf-8") as f:
                    self.wfile.write(bytes(f.read(), "utf-8"))
            except FileNotFoundError:
                self.wfile.write(bytes("<h1>Server Ready</h1>", "utf-8"))
            return

        status = 200
        content_type = "application/json" if is_json else "text/html"
        contents = ""

        try:
            if path == "/listSpecies":
                limit_param = (
                    arguments["limit"][0] if "limit" in arguments else None
                )
                conn = http.client.HTTPSConnection(SERVER)
                conn.request(
                    "GET",
                    f"/info/species{PARAMS}",
                    headers={"Content-Type": "application/json"},
                )
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                species_list = d["species"]
                total_species = len(species_list)
                if limit_param:
                    species_list = species_list[: int(limit_param)]

                names_list = [
                    f"{s['display_name']} ({s['name']})" for s in species_list
                ]
                dic_species = {
                    "Limit": int(limit_param) if limit_param else total_species,
                    "names": names_list,
                    "num_species": total_species,
                }
                contents = (
                    json.dumps(dic_species)
                    if is_json
                    else f"<ul>"
                    + "".join([f"<li>{n}</li>" for n in names_list])
                    + "</ul>"
                )

            elif path == "/karyotype":
                species = arguments["species"][0]
                conn = http.client.HTTPSConnection(SERVER)
                conn.request(
                    "GET",
                    f"/info/assembly/{species}{PARAMS}",
                    headers={"Content-Type": "application/json"},
                )
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                karyotype_data = d.get("karyotype", [])
                contents = (
                    json.dumps(karyotype_data)
                    if is_json
                    else f"<ul>"
                    + "".join([f"<li>{c}</li>" for c in karyotype_data])
                    + "</ul>"
                )

            elif path == "/chromosomeLength":
                species = arguments["species"][0]
                chromo = arguments["chromo"][0]
                conn = http.client.HTTPSConnection(SERVER)
                conn.request(
                    "GET",
                    f"/info/assembly/{species}{PARAMS}",
                    headers={"Content-Type": "application/json"},
                )
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                regions = d.get("top_level_region", [])
                length = None
                for r in regions:
                    if str(r["name"]).lower() == str(chromo).lower():
                        length = r["length"]

                if length is None:
                    raise Exception()
                contents = (
                    json.dumps({"length": length})
                    if is_json
                    else f"Length: {length}"
                )

            elif path == "/geneLookup":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)
                if not gene_id:
                    raise Exception()
                contents = (
                    json.dumps({"gene": gene, "gene_id": gene_id})
                    if is_json
                    else f"ID: {gene_id}"
                )

            elif path == "/geneSeq":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)
                if not gene_id:
                    raise Exception()
                conn = http.client.HTTPSConnection(SERVER)
                conn.request(
                    "GET",
                    f"/sequence/id/{gene_id}{PARAMS}",
                    headers={"Content-Type": "application/json"},
                )
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                sequence = d.get("seq", "")
                contents = (
                    json.dumps({"gene": gene, "seq": sequence})
                    if is_json
                    else f"<p>{sequence}</p>"
                )

            elif path == "/geneInfo":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)
                if not gene_id:
                    raise Exception()
                conn = http.client.HTTPSConnection(SERVER)
                conn.request(
                    "GET",
                    f"/lookup/id/{gene_id}{PARAMS}",
                    headers={"Content-Type": "application/json"},
                )
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                dic_info = {
                    "start": int(d["start"]),
                    "end": int(d["end"]),
                    "length": int(d["end"]) + 1 - int(d["start"]),
                    "id": gene_id,
                    "gene": gene,
                    "chromo": d["seq_region_name"],
                }
                contents = (
                    json.dumps(dic_info)
                    if is_json
                    else f"<p>{dic_info['id']}</p>"
                )

            elif path == "/geneCalc":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)
                if not gene_id:
                    raise Exception()
                conn = http.client.HTTPSConnection(SERVER)
                conn.request(
                    "GET",
                    f"/sequence/id/{gene_id}{PARAMS}",
                    headers={"Content-Type": "application/json"},
                )
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                sequence = d.get("seq", "")
                clean_seq = "".join(sequence.split()).upper()
                total = len(clean_seq)
                counts = {
                    "A": clean_seq.count("A"),
                    "C": clean_seq.count("C"),
                    "G": clean_seq.count("G"),
                    "T": clean_seq.count("T"),
                }
                contents = (
                    json.dumps({"gene": gene, "length": total, "seq_count": counts})
                    if is_json
                    else f"<p>Length: {total}</p>"
                )

                # 8) ENDPOINT: GENE LIST (Desglose detallado de atributos de Ensembl)
                elif path == "/geneList":
                chromo = arguments["chromo"][0]
                start = arguments["start"][0]
                end = arguments["end"][0]

                ENDPOINT = f"/overlap/region/homo_sapiens/{chromo}:{start}-{end}{PARAMS}&feature=gene"
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", ENDPOINT, headers={"Content-Type": "application/json"})
                gene_data = json.loads(conn.getresponse().read().decode())
                conn.close()

                unique_genes = []
                seen = set()

                # Extraemos los IDs de los genes de forma segura
                for item in gene_data:
                    gene_id = item.get("id")
                    if gene_id and gene_id not in seen:
                        seen.add(gene_id)
                        unique_genes.append(gene_id)

                # Diccionario limpio que necesita tu cliente
                dic_gene_list = {
                    "chromosome": chromo,
                    "start": int(start),
                    "end": int(end),
                    "genes": unique_genes,
                }

                if is_json:
                    contents = json.dumps(dic_gene_list)
                else:
                    # Formato web limpio: si hay genes los pinta en una lista, si no, avisa
                    if unique_genes:
                        contents = "<h2>Genes found in region:</h2><ul>" + "".join(
                            [f"<li>{g}</li>" for g in unique_genes]) + "</ul>"
                    else:
                        contents = "<h2>No genes found in this region.</h2>"

            else:
                status = 404
                contents = "Not Found"

            except Exception as e:
            status = 500
            contents = f"Error: {str(e)}"

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(bytes(contents, "utf-8"))
if __name__ == "__main__":
    # Usamos allow_reuse_address para evitar el típico error de puerto ocupado
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
        print(f"Serving at port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")