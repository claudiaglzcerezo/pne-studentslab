import http.client
import http.server
import json
import socketserver
import urllib.parse

PORT = 8080
SERVER = "rest.ensembl.org"
PARAMS = "?content-type=application/json"


class TestHandler(http.server.BaseHTTPRequestHandler):

    #ID ESTABLE DE UN GEN
    def get_id(self, arguments):
        try:
            gene_symbol = arguments["gene"][0]
            species = arguments["species"][0].strip().lower()
            ENDPOINT = f"/lookup/symbol/{species}/{gene_symbol}"
            conn = http.client.HTTPSConnection(SERVER)
            conn.request("GET", ENDPOINT + PARAMS, headers={"Content-Type": "application/json"})
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

        #index
        if path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            try:
                with open("indexSIMU.html", "r", encoding="utf-8") as f:
                    self.wfile.write(bytes(f.read(), "utf-8"))
            except FileNotFoundError:
                self.wfile.write(bytes("<h1>Server Ready</h1>", "utf-8"))
            return

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
                names_list = []
                for s in species_list:
                    text_specie = f"{s['display_name']} ({s['name']})"
                    names_list.append(text_specie)
                if limit_param:
                    limite_final = int(limit_param)
                else:
                    limite_final = total_species
                dic_species = {
                    "Limit": limite_final,
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
            elif path == "/sequences":
                eid = arguments["id"]
                spe = arguments["query"]

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
            #GENE SYMBOL PRUEBAS
            elif path == "/geneSymbol":
                if "species" not in arguments:
                    raise Exception()
                spe = arguments["species"][0].strip().lower()
                if not spe:
                    raise Exception()
                if "symbol" in arguments:
                    sym = arguments["symbol"][0].strip().upper()
                else:
                    sym = "BRCA2"

                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/lookup/symbol/{spe}/{sym}{PARAMS}", headers={"Content-type":"application/json"})
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                if not d or "error" in d:
                    raise Exception()
                gene_id = d.get("id")
                bio = d.get("biotype")
                display_sym = d.get("display_name", sym)
                if not gene_id or not bio:
                    raise Exception()

                dic_info = {
                "specie": spe,
                "symbol": display_sym,
                "id": gene_id,
                "biotype": bio,
                }
                if is_json:
                    contents = json.dumps(dic_info)
                else:

                    contents = (
                f"<h2>Return information about a human gene:</h2>"
                f"<ul>"
                f"<li><b>Specie:</b> {spe}</li>"
                f"<li><b>Symbol:</b> {sym}</li>"
                f"<li><b>ID:</b> {gene_id}</li>"
                f"<li><b>Biotype:</b> {bio}</li>"
                f"</ul>"
            )

            #GEN ID PRUEBA
            elif path == "/geneId":
                if "display_name" not in arguments or "description" not in arguments:
                    raise Exception()
                name = arguments["display_name"][0].upper()
                desc = arguments["description"][0].upper()
                if not name or not desc:
                    raise Exception()

                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/lookup/symbol/{name}/{desc}", headers={"Content-type=application/json"})
                d = json.loads(conn.getresponse().read().decode())
                conn.close()
                if not d or "error" in d:
                    raise Exception()
                gene_id = d.get("id")
                if not gene_id:
                    raise Exception()
                dic_info = {
                    "name": name,
                    "description": desc,
                    "id": gene_id,
                }
                if is_json:
                    contents = json.dumps(dic_info)
                else:

                    contents = (
                        f"<h2>Return information about a human gene:</h2>"
                        f"<ul>"
                        f"<li><b>Name:</b> {name}</li>"
                        f"<li><b>description:</b> {desc}</li>"
                        f"<li><b>ID:</b> {gene_id}</li>"
                        f"</ul>"
                    )
            #GENEGc PRUEBA
            elif path == "/geneGc":
                if "id" not in arguments:
                    raise Exception()
                gene = arguments["id"][0].upper()
                if not gene:
                    raise Exception()
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/sequence/id/{gene}{PARAMS}", headers={"Content-Type": "application/json"})
                d = json.loads(conn.getresponse().read().decode())
                conn.close()
                if not d or "error" in d:
                    raise Exception()
                n = d.get("seq", "")
                clean_seq = "".join(n.split()).upper()
                total = len(clean_seq)

                count_c = clean_seq.count("C")
                count_g = clean_seq.count("G")

                # porcentajes
                if total > 0:
                    pct_c = (count_c * 100) / total
                    pct_g = (count_g * 100) / total
                else:
                    pct_c = 0
                    pct_g = 0

                dic_calc = {
                    "gene id": gene,
                    "length": total,
                    "seq_count": {"C": count_c, "G": count_g}
                }

                if is_json:
                    contents = json.dumps(dic_calc)
                else:
                    contents = (
                        f"<h2>Performs some calculations on the provided human gene returning the total length and the percentage of all the bases:</h2>"
                        f"<ul>"
                        f"<li><b>Total Length:</b> {total} bases</li>"
                        f"<li><b>% C:</b> {pct_c:.2f}%</li>"
                        f"<li><b>% G:</b> {pct_g:.2f}%</li>"
                        f"</ul>"
                    )
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
            # 6) GENE INFO
            elif path == "/geneInfo":
                gene = arguments["gene"][0].upper()
                gene_id = self.get_id(arguments)
                if not gene_id:
                    raise Exception()

                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", f"/lookup/id/{gene_id}{PARAMS}", headers={"Content-Type": "application/json"})
                d = json.loads(conn.getresponse().read().decode())
                conn.close()

                # datos
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

            # 7) GENE CALC
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

                #porcentajes
                if total > 0:
                    pct_a = (count_a * 100) / total
                    pct_c = (count_c * 100) / total
                    pct_g = (count_g * 100) / total
                    pct_t = (count_t * 100) / total
                else:
                    pct_a = 0
                    pct_c = 0
                    pct_g = 0
                    pct_t = 0

                dic_calc = {
                    "gene": gene,
                    "length": total,
                    "seq_count": {"A": count_a, "C": count_c, "G": count_g, "T": count_t}
                }

                if is_json:
                    contents = json.dumps(dic_calc)
                else:
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

            #EXAMEN PRUEBA 2
            elif path == "/gene_homologies":
                gene = arguments['gene'][0].strip()
                limit_r = arguments['limit'][0].strip()
                if not gene or not limit_r:
                    raise Exception('Please enter a value')
                limit = int(limit_r)
                ENDPOINT = f"/homology/id/{gene}?content-type=application/json"
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", ENDPOINT, headers={"Content-Type": "application/json"})
                d = json.loads(conn.getresponse().read().decode())
                conn.close()
                if 'error' in d:
                    raise Exception()
                homologies = d['data'][0]['homologies']

                if len(homologies) > limit:
                    m = homologies[0:limit]
                else:
                    m = homologies

                lista_tipos = []
                lista_especies = []
                lista_ids = []

                count = 0
                while count < limit and count < len(m):
                    # 1. Sacamos el animal que toca en esta vuelta (esto es un diccionario)
                    homologo = m[count]
                    # 2. Sacamos el tipo directamente de ese animal
                    type_val = homologo.get('type', 'Unknown')
                    # 3. Sacamos el diccionario 'target' directamente (sin bucles for)
                    info = homologo.get('target', {})
                    # 4. Extraemos los campos de dentro de 'info'
                    name_val = info.get('species', 'Unknown')
                    id_val = info.get('id', 'No ID')
                    # 5. Los guardamos en nuestras listas limpias
                    lista_tipos.append(type_val)
                    lista_especies.append(name_val)
                    lista_ids.append(id_val)
                    count += 1
                with open('gene_homologies.html', 'r', encoding='utf-8') as f:
                    template = f.read()
                    contents = template.format(
                        types=lista_tipos,
                        species=lista_especies,
                        ids=lista_ids
                    )





            #EXAM MAY
            elif path == "/compare_genes":
                id1 = arguments["g1"][0].strip()
                id2 = arguments["g2"][0].strip()
                if not id1 or not id2:
                    raise Exception()

                    # Asegúrate de concatenar o escribir directamente ?expand=1 al final de la URL
                ENDPOINT1 = f"/lookup/id/{id1}?expand=1"
                ENDPOINT2 = f"/lookup/id/{id2}?expand=1"
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", ENDPOINT1, headers={"Content-Type": "application/json"})
                d1 = json.loads(conn.getresponse().read().decode())

                conn.request("GET", ENDPOINT2, headers={"Content-Type": "application/json"})
                d2 = json.loads(conn.getresponse().read().decode())

                conn.close()
                if "error" in d1 or "error" in d2:
                    raise Exception()
                name1 = d1.get("display_name", id1)
                transcript1 = d1.get("Transcript", [])
                number_t1 = len(transcript1)

                max_e1 = 0
                for g in transcript1:
                    exon1 = g.get("Exon", [])
                    if max_e1 < len(exon1):
                        max_e1 = len(exon1)


                name2 = d2.get("display_name", id2)
                transcript2 = d2.get("Transcript", [])
                number_t2 = len(transcript2)

                max_e2 = 0
                for p in transcript2:
                    exon2 = p.get("Exon", [])
                    if max_e2 < len(exon2):
                        max_e2 = len(exon2)



                if number_t1 > number_t2:
                    diff = number_t1 - number_t2
                    winner = f"{name1} is more complex, containing {diff} more transcripts than {name2}."
                elif number_t2 > number_t1:
                    diff = number_t2 - number_t1
                    winner = f"{name2} is more complex, containing {diff} more transcripts than {name1}."
                else:
                    winner = f"Both genes are equally complex, containing the same number of transcripts ({number_t1})."

                with open("compare_genes.html", "r", encoding="utf-8") as f:
                    template = f.read()

                contents = template.format(
                    name_g1 = name1,
                    lenght_g1=f"{number_t1}",
                    exon_g1=f"{max_e1}",
                    name_g2=name2,
                    lenght_g2=f"{number_t2}",
                    exon_g2=f"{max_e2}",
                    winner=f"{winner}"
                )
            #SIMULACRO GENE DISEASE
            elif path == "/gene_diseases":
                gene = arguments['gene'][0].strip()
                limit = int(arguments['limit'][0].strip())
                if not gene or not limit:
                    raise Exception()
                ENDPOINT = f"/phenotype/gene/homo_sapiens/{gene}?content-type=application/json"
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", ENDPOINT, headers={"Content-Type": "application/json"})
                g = json.loads(conn.getresponse().read().decode())
                conn.close()
                if 'error' in g or not g.get('data'):
                    raise Exception()

                total = len(g)
                if len(g) > limit:
                    lst = g[0:limit]
                else:
                    lst = g

                # Creamos 3 listas de Python vacías para guardar solo el texto limpio
                lista_nombres = []
                lista_ids = []
                lista_fuentes = []

                # Recorremos los datos con el while académico (sin usar break ni HTML)
                count= 0
                while count < limit and count < total:
                    enfermedad = g[count]


                    name_val = enfermedad.get('description', 'No description')
                    id_val = enfermedad.get('id', 'No ID')
                    source_val = enfermedad.get('source', 'Unknown')

                    # Los añadimos limpios a nuestras listas de Python
                    lista_nombres.append(name_val)
                    lista_ids.append(id_val)
                    lista_fuentes.append(source_val)

                    count += 1
                # 3. Abrimos tu plantilla externa
                with open("gene_diseases.html", "r", encoding="utf-8") as f:
                    template = f.read()

                # 4. Le pasamos al HTML la lista ya recortada
                contents = template.format(
                    gene=gene,
                    total=total,
                    resultados=lst
                )

            elif path == '/sequence_quality':
                region = arguments['region'][0].strip()
                if not region:
                    raise Exception('Please enter a region')
                ENDPOINT = f"/sequence/region/human/{region}?content-type=application/json"
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", ENDPOINT, headers={"Content-Type": "application/json"})
                d = json.loads(conn.getresponse().read().decode())
                conn.close()
                if 'error' in d or not d:
                    raise Exception('There must be a problem with the URL')
                seq = d.get('seq')
                total = len(seq)

                countG = []
                countC = []
                count = 0
                while count < total:
                    base = seq[count]
                    if base == 'G':
                        countG.append(base)
                    elif base == 'C':
                        countC.append(base)
                    count = count + 1
                nG = len(countG)
                nC = len(countC)
                pctj = round((nG + nC) * 100 / total, 2)

                with open('sequence_quality.html', 'r', encoding='utf-8') as f:
                    template = f.read()
                    contents = template.format(
                        SeqLength= total,
                        percentage=pctj
                    )
            elif path == '/classify_genes':
                region = arguments['region'][0].strip()
                if not region:
                    raise Exception('Please enter a region')
                ENDPOINT = f"/overlap/region/human/{region}?feature=gene&content-type=application/json"
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", ENDPOINT, headers={"Content-Type": "application/json"})
                g = json.loads(conn.getresponse().read().decode())
                conn.close()
                if 'error' in g:
                    raise Exception('The URL is not valid')
                lngth_d = len(g)
                count = 0
                lst_reverse = []
                lst_forward =  []
                while lngth_d > count:
                    m = g[count]
                    name = m.get('external_name')
                    strand = m.get('strand')
                    if strand == 1:
                        lst_forward.append(name)
                    elif strand == -1:
                        lst_reverse.append(name)
                    count = count + 1

                with open('classify_genes.html', 'r', encoding='utf-8') as f:
                    template = f.read()
                    contents = template.format(
                        lst_f=lst_forward,
                        lst_r=lst_reverse
                    )
            elif path == '/exon_density':
                chr = arguments['chromo'][0].strip()
                start = int(arguments["start"][0].strip())
                end = int(arguments["end"][0].strip())
                if not chr or not start or not end:
                    raise Exception('Please fill the gaps')
                ENDPOINT = f'/overlap/region/human/{chr}:{start}-{end}?feature=exon&content-type=application/json'
                conn = http.client.HTTPSConnection(SERVER)
                conn.request("GET", ENDPOINT, headers={"Content-Type": "application/json"})
                g = json.loads(conn.getresponse().read().decode())
                conn.close()
                if 'error' in g:
                    raise Exception('Not valid URL')
                length_lst = len(g)
                count = 0
                length_sum = 0
                lst = []
                while count < length_lst:
                    exon = g[count]
                    start1 = exon['start']
                    end1 = exon['end']
                    exon_id = exon.get('id')
                    length_exon = end1 - start1 + 1
                    m = exon.get('strand')
                    if m == 1 and length_exon > 200:
                        lst.append(exon_id)
                        length_sum = length_sum + length_exon
                    count = count + 1

                    if len(lst) > 0:
                        ptcj = length_sum / len(lst)
                        ptj = round(ptcj, 2)
                    else:
                        ptj = 0.0

                    with open('exon_density.html', 'r', encoding='utf-8') as f:
                        template = f.read()

                    contents = template.format(
                        region=f"{chr}:{start}-{end}",
                        count=len(lst),
                        avg=ptj
                        )









            # 8) ENDPOINT: GENE LIST
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
                        name = item.get("external_name")
                        if name:
                            display_text = f"{name} ({gene_id})"
                        else:
                            display_text = f"{gene_id}"
                        html_lines.append(f"<li>{display_text}</li>")


                dic_gene_list = {
                    "chromosome": chromo,
                    "start": int(start),
                    "end": int(end),
                    "genes": unique_genes,
                }

                if is_json:
                    contents = json.dumps(dic_gene_list)
                else:
                    if html_lines:
                        contents = f"<h2>Genes found in region {chromo}:{start}-{end}:</h2><ul>" + "".join(
                            html_lines) + "</ul>"
                    else:
                        contents = f"<h2>No genes found in region {chromo}:{start}-{end}.</h2>"
            else:
                status = 404
                contents = "Not Found"

        except Exception as e:
            status = 500
            contents = f"<html><body style='color: red;'><h2>An error has occurred</h2><p>{str(e)}</p></body></html>"
        if status == 500:
            content_type = "text/html"
            import os
            if os.path.exists("error.html"):
                with open("error.html", "r", encoding="utf-8") as f:
                    contents = f.read()
        if status == 200 and (contents == "" or contents == "<ul></ul>"):
            contents = "<h2>No data found. Please check if the species or parameters are correct.</h2>"
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