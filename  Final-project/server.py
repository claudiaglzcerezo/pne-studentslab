import http.server
import socketserver
import urllib.parse
import http.client
import json
from pathlib import Path

PORT = 8080
SERVER = "rest.ensembl.org"
PARAMS = "?content-type=application/json"


class TestHandler(http.server.BaseHTTPRequestHandler):

    # FUNCIÓN INTERNA PARA OBTENER EL ID ESTABLE DE UN GEN
    def get_id(self, arguments):
        gene_symbol = arguments["gene"][0]
        ENDPOINT = f"/lookup/symbol/homo_sapiens/{gene_symbol}"

        conn = http.client.HTTPSConnection(SERVER)
        conn.request("GET", ENDPOINT + PARAMS)
        response = conn.getresponse()
        data = response.read().decode()
        d = json.loads(data)
        conn.close()

        if d and "id" in d:
            return d["id"]
        return None

    # PROCESAMIENTO DE PETICIONES GET
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        arguments = urllib.parse.parse_qs(parsed_url.query)

        is_json = "json" in arguments

        # PÁGINA DE INICIO (INDEX.HTML)
        if path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open("index.html", "r", encoding="utf-8") as f:
                self.wfile.write(bytes(f.read(), "utf-8"))
            return

        try:
            status = 200
            contents = ""
            content_type = "application/json" if is_json else "text/html"

            # #BASIC LEVEL

            # 1) LIST SPECIES
            if path == "/listSpecies":
                limit_param = arguments["limit"][0] if "limit" in arguments else None

                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/info/species{PARAMS}")
                response = conn.getresponse()
                d = json.loads(response.read().decode())
                conn.close()

                species_list = d["species"]
                total_species = len(species_list)
                if limit_param:
                    species_list = species_list[:int(limit_param)]

                names_list = [f"{s['display_name']} ({s['name']})" for s in species_list]

                dic_species = {
                    "Limit": int(limit_param) if limit_param else total_species,
                    "names": names_list,
                    "num_species": total_species
                }

                if is_json:
                    contents = json.dumps(dic_species)
                else:
                    contents = "<ul>" + "".join([f"<li>{name}</li>" for name in names_list]) + "</ul>"

            # 2) KARYOTYPE
            elif path == "/karyotype":
                species = arguments["species"][0]

                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/info/assembly/{species}{PARAMS}")
                response = conn.getresponse()
                d = json.loads(response.read().decode())
                conn.close()

                karyotype_data = d["karyotype"]
                if is_json:
                    contents = json.dumps(karyotype_data)
                else:
                    contents = f"<p>Chromosomes:</p><ul>" + "".join(
                        [f"<li>Chromosome {c}</li>" for c in karyotype_data]) + "</ul>"

            # 3) CHROMOSOME LENGTH (CON BUCLE FOR SIN BREAK)
            elif path == "/chromosomeLength":
                species = arguments["species"][0]
                chromo = arguments["chromo"][0]

                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/info/assembly/{species}{PARAMS}")
                response = conn.getresponse()
                d = json.loads(response.read().decode())
                conn.close()

                regions = d["top_level_region"]

                length = None
                for r in regions:
                    if str(r["name"]).lower() == str(chromo).lower():
                        length = r["length"]

                if length is None:
                    raise Exception()

                dic_len = {"length": length}
                if is_json:
                    contents = json.dumps(dic_len)
                else:
                    contents = f"The length of the chromosome is: {length}"

            # #MEDIUM LEVEL

            # 4) GENE LOOKUP
            elif path == "/geneLookup":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)

                if gene_id:
                    dic_lookup = {"gene": gene, "gene_id": gene_id}
                    if is_json:
                        contents = json.dumps(dic_lookup)
                    else:
                        contents = f"Stable ID: {gene_id}"
                else:
                    raise Exception()

            # 5) GENE SEQ (LONGITUD CON LEN)
            elif path == "/geneSeq":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)

                if not gene_id:
                    raise Exception()

                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/sequence/id/{gene_id}{PARAMS}")
                response = conn.getresponse()
                d = json.loads(response.read().decode())
                conn.close()

                sequence = d["seq"]
                dic_seq = {"gene": gene, "seq": sequence}

                if is_json:
                    contents = json.dumps(dic_seq)
                else:
                    contents = f"<textarea style='width:100%;height:150px;' readonly>{sequence}</textarea>"

            # 6) GENE INFO (LONGITUD RESTANDO END + 1 - START)
            elif path == "/geneInfo":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)

                if not gene_id:
                    raise Exception()

                ENDPOINT = f"/lookup/id/{gene_id}"
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", ENDPOINT + PARAMS)
                response = conn.getresponse()
                d = json.loads(response.read().decode())
                conn.close()

                dic_info = {
                    "start": d["start"],
                    "end": d["end"],
                    "length": int(d["end"]) + 1 - int(d["start"]),
                    "id": gene_id,
                    "gene": gene,
                    "chromo": d["seq_region_name"]
                }

                if is_json:
                    contents = json.dumps(dic_info)
                else:
                    contents = (
                        f"<h2>Return information about a human gene:</h2>"
                        f"<ul>"
                        f"<li><b>ID:</b> {dic_info['id']}</li>"
                        f"<li><b>Chromosome:</b> {dic_info['chromo']}</li>"
                        f"<li><b>Start:</b> {dic_info['start']}</li>"
                        f"<li><b>End:</b> {dic_info['end']}</li>"
                        f"<li><b>Length:</b> {dic_info['length']}</li>"
                        f"</ul>"
                    )

            # 7) GENE CALC (CORREGIDO SIN IMPORTAR RE)
            elif path == "/geneCalc":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)

                if not gene_id:
                    raise Exception()

                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/sequence/id/{gene_id}{PARAMS}")
                response = conn.getresponse()
                d = json.loads(response.read().decode())
                conn.close()

                sequence = d["seq"]

                # LIMPIAMOS LA SECUENCIA USANDO MÉTODOS NATIVOS DE STRING
                clean_seq = "".join(sequence.split()).upper()
                total = len(clean_seq)

                counts = {
                    "A": clean_seq.count("A"),
                    "C": clean_seq.count("C"),
                    "G": clean_seq.count("G"),
                    "T": clean_seq.count("T")
                }

                dic_calc = {"gene": gene, "length": total, "seq_count": counts}
                if is_json:
                    contents = json.dumps(dic_calc)
                else:
                    pct_a = (counts["A"] * 100) / total
                    pct_c = (counts["C"] * 100) / total
                    pct_g = (counts["G"] * 100) / total
                    pct_t = (counts["T"] * 100) / total

                    contents = (
                        f"<h2>Performs some calculations on the provided human gene returning the total length and the percentage of all the bases:</h2>"
                        f"<ul>"
                        f"<li><b>Total Length:</b> {total} bases</li>"
                        f"<li><b>% A:</b> {pct_a:.2f}%</li>"
                        f"<li><b>% C:</b> {pct_c:.2f}%</li>"
                        f"<li><b>% G:</b> {pct_g:.2f}%</li>"
                        f"<li><b>% T:</b> {pct_t:.2f}%</li>"
                        f"</ul>"
                    )



            elif path == "/geneList":
                chromo = arguments["chromo"][0]
                start = arguments["start"][0]
                end = arguments["end"][0]

                # Consultamos la API de Ensembl para la región en humanos
                # Agregamos feature=gene para traer solo los genes de la región
                ENDPOINT = f"/overlap/region/homo_sapiens/{chromo}:{start}-{end}{PARAMS}&feature=gene"

                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", ENDPOINT)
                response = conn.getresponse()
                gene_data = json.loads(response.read().decode())
                conn.close()

                # Extraemos los nombres de manera única sin usar dict.fromkeys
                unique_genes = []
                seen = set()

                for item in gene_data:
                    # Obtenemos el nombre del gen (o el ID si no tiene nombre)
                    name = item.get("external_name") or item.get("id")

                    if name and name not in seen:
                        seen.add(name)
                        unique_genes.append(name)

                dic_gene_list = {
                    "chromosome": chromo,
                    "start": start,
                    "end": end,
                    "genes": unique_genes,
                }

                if is_json:
                    contents = json.dumps(dic_gene_list)
                else:
                    contents = (
                            f"<h2>Genes in region {chromo}:{start}-{end}:</h2>"
                            f"<ul>"
                            + "".join([f"<li>{g}</li>" for g in unique_genes])
                            + "</ul>"
                    )
        except Exception as e:
            status = 500
            contents = f"<h1>Error detectado en el Servidor:</h1><p>{str(e)}</p>"
            self.send_response(status)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(contents, "utf-8"))

        # GESTIÓN GLOBAL DE ERRORES (ERROR.HTML)


# ARRANQUE DEL SERVIDOR
if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
        print(f"Server online on port {PORT}...")
        httpd.serve_forever()