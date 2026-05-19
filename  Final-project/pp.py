import http.client
import http.server
import json
import socketserver
import urllib.parse

PORT = 8080
SERVER = "rest.ensembl.org"
PARAMS = "?content-type=application/json"


class TestHandler(http.server.BaseHTTPRequestHandler):

    # FUNCIÓN INTERNA PARA OBTENER EL ID ESTABLE DE UN GEN
    def get_id(self, arguments):
        try:
            gene_symbol = arguments["gene"][0]
            ENDPOINT = f"/lookup/symbol/homo_sapiens/{gene_symbol}"
            conn = http.client.HTTPSConnection(SERVER)
            conn.request("GET", ENDPOINT + PARAMS, headers={"Content-Type": "application/json"})
            response = conn.getresponse()
            d = json.loads(response.read().decode())
            conn.close()
            return d.get("id")
        except Exception:
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
            try:
                with open("index.html", "r", encoding="utf-8") as f:
                    self.wfile.write(bytes(f.read(), "utf-8"))
            except FileNotFoundError:
                self.wfile.write(bytes("<h1>Server Ready</h1>", "utf-8"))
            return

        # ASIGNACIÓN DE VARIABLES DE SALIDA
        status = 200
        content_type = "application/json" if is_json else "text/html"
        contents = ""

        try:
            # 1) LIST SPECIES
            if path == "/listSpecies":
                limit_param = arguments["limit"][0] if "limit" in arguments else None
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/info/species{PARAMS}", headers={"Content-Type": "application/json"})
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                species_list = d["species"]
                total_species = len(species_list)
                if limit_param:
                    species_list = species_list[: int(limit_param)]

                names_list = [f"{s['display_name']} ({s['name']})" for s in species_list]
                dic_species = {
                    "Limit": int(limit_param) if limit_param else total_species,
                    "names": names_list,
                    "num_species": total_species,
                }
                contents = json.dumps(dic_species) if is_json else f"<ul>" + "".join(
                    [f"<li>{n}</li>" for n in names_list]) + "</ul>"

            # 2) KARYOTYPE
            elif path == "/karyotype":
                species = arguments["species"][0]
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/info/assembly/{species}{PARAMS}", headers={"Content-Type": "application/json"})
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                karyotype_data = d.get("karyotype", [])
                contents = json.dumps(karyotype_data) if is_json else f"<ul>" + "".join(
                    [f"<li>{c}</li>" for c in karyotype_data]) + "</ul>"

            # 3) CHROMOSOME LENGTH
            elif path == "/chromosomeLength":
                species = arguments["species"][0]
                chromo = arguments["chromo"][0]
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/info/assembly/{species}{PARAMS}", headers={"Content-Type": "application/json"})
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                regions = d.get("top_level_region", [])
                length = None
                for r in regions:
                    if str(r["name"]).lower() == str(chromo).lower():
                        length = r["length"]

                if length is None:
                    raise Exception()
                contents = json.dumps({"length": length}) if is_json else f"Length: {length}"

            # 4) GENE LOOKUP
            elif path == "/geneLookup":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)
                if not gene_id:
                    raise Exception()
                contents = json.dumps({"gene": gene, "gene_id": gene_id}) if is_json else f"ID: {gene_id}"

            # 5) GENE SEQ
            elif path == "/geneSeq":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)
                if not gene_id:
                    raise Exception()
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/sequence/id/{gene_id}{PARAMS}", headers={"Content-Type": "application/json"})
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                sequence = d.get("seq", "")
                contents = json.dumps({"gene": gene, "seq": sequence}) if is_json else f"<p>{sequence}</p>"

            # 6) GENE INFO (ARREGLADO PARA IMPRIMIR TODO EN LA WEB)
            elif path == "/geneInfo":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)
                if not gene_id:
                    raise Exception()

                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/lookup/id/{gene_id}{PARAMS}", headers={"Content-Type": "application/json"})
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                # Extraemos los datos solicitados
                start_val = int(d["start"])
                end_val = int(d["end"])
                length_val = end_val + 1 - start_val
                chromo_name = d["seq_region_name"]

                dic_info = {
                    "start": start_val,
                    "end": end_val,
                    "length": length_val,
                    "id": gene_id,
                    "gene": gene,
                    "chromo": chromo_name,
                }

                if is_json:
                    contents = json.dumps(dic_info)
                else:
                    # Formato web exacto solicitado
                    contents = (
                        f"<h2>Return information about a human gene:</h2>"
                        f"<ul>"
                        f"<li><b>Start:</b> {start_val}</li>"
                        f"<li><b>End:</b> {end_val}</li>"
                        f"<li><b>Length:</b> {length_val}</li>"
                        f"<li><b>ID:</b> {gene_id}</li>"
                        f"<li><b>Chromosome name:</b> {chromo_name}</li>"
                        f"</ul>"
                    )

            # 7) GENE CALC (ARREGLADO PARA IMPRIMIR TODO EN LA WEB)
            elif path == "/geneCalc":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)
                if not gene_id:
                    raise Exception()

                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/sequence/id/{gene_id}{PARAMS}", headers={"Content-Type": "application/json"})
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                sequence = d.get("seq", "")
                clean_seq = "".join(sequence.split()).upper()
                total = len(clean_seq)

                # Contamos bases individuales
                count_a = clean_seq.count("A")
                count_c = clean_seq.count("C")
                count_g = clean_seq.count("G")
                count_t = clean_seq.count("T")

                # Calculamos porcentajes
                pct_a = (count_a * 100) / total if total > 0 else 0
                pct_c = (count_c * 100) / total if total > 0 else 0
                pct_g = (count_g * 100) / total if total > 0 else 0
                pct_t = (count_t * 100) / total if total > 0 else 0

                dic_calc = {
                    "gene": gene,
                    "length": total,
                    "seq_count": {"A": count_a, "C": count_c, "G": count_g, "T": count_t}
                }

                if is_json:
                    contents = json.dumps(dic_calc)
                else:
                    # Formato web exacto solicitado con porcentajes
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

            # 8) ENDPOINT: GENE LIST
                    # 8) ENDPOINT: GENE LIST (Formateado para mostrar Nombre e ID en el Navegador)
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
                html_lines = []
                seen = set()

                for item in gene_data:
                    gene_id = item.get("id")
                    if gene_id and gene_id not in seen:
                        seen.add(gene_id)
                        unique_genes.append(gene_id)

                        # Extraemos el nombre común si existe (ej: CDKN2A)
                        name = item.get("external_name")

                        # Si tiene nombre común, guardamos "Nombre (ID)". Si no, solo el ID.
                        if name:
                            display_text = f"{name} ({gene_id})"
                        else:
                            display_text = f"{gene_id}"

                        # Lo metemos en una etiqueta de lista HTML
                        html_lines.append(f"<li>{display_text}</li>")

                # El diccionario estructurado que necesita tu cliente.py de forma obligatoria
                dic_gene_list = {
                    "chromosome": chromo,
                    "start": int(start),
                    "end": int(end),
                    "genes": unique_genes,
                }

                if is_json:
                    contents = json.dumps(dic_gene_list)
                else:
                    # Si entras desde el navegador (no json), te dibuja la lista con los nombres e IDs
                    if html_lines:
                        contents = f"<h2>Genes found in region {chromo}:{start}-{end}:</h2><ul>" + "".join(
                            html_lines) + "</ul>"
                    else:
                        contents = f"<h2>No genes found in region {chromo}:{start}-{end}.</h2>"
        except Exception as e:
            status = 500
            contents = f"Error: {str(e)}"
        # ENVÍO CRÍTICO DE LA VARIABLE CONTENTS AL NAVEGADOR
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(bytes(contents, "utf-8"))


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
        print(f"Serving at port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")