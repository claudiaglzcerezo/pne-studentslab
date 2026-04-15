import http.server
import socketserver
import jinja2 as j
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT = 8080

SEQUENCES = [
    "ACCAACTGACTGAAACCCGGGACTACTACTACTTTAGGGGGTTTCCCAGGATCTCGATCA",
    "TATTTGGGGACCCCCCCCCCCTTTTTTTGGGGAGAGAGAACTCTCTTTTCCCCCTGGGCG",
    "CCCGTGAACCCTTCTTCAAAAGAGAGAGTGTGTGTTCATTTCCCTAATCTCCGTATTTTT",
    "GGGGCCTGACTCCAATATTTCCCCAAAGTGTGGTGTTGTTGTTAAAAGCCGGACCTCAAA",
    "AGCGCAAACGCTAAAAACCGGTTGAGTTGACGCACGGAGAGAAGGGGTGTGTGGGTGGGT"
]
genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]


def read_html_file(filename):
    # Lee el archivo desde la carpeta html/
    contents = Path("html/" + filename).read_text()
    # Crea la plantilla de Jinja2
    contents = j.Template(contents)
    return contents


class SeqHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Parseamos la URL para extraer la ruta y los parámetros
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        params = parse_qs(parsed_url.query)

        try:
            # --- Ejercicio 1: PING ---
            if path == "/ping":
                template = read_html_file("index.html")
                # En index.html no solemos pasar variables, pero se renderiza igual
                content = template.render()
                self.send_response_200(content)

            # --- Ejercicio 2: GET (/get?id=X) ---
            elif path == "/get":
                # Extraemos el id (por defecto el primero de la lista de params)
                idx = int(params.get('id', [0])[0])

                if 0 <= idx < len(SEQUENCES):
                    seq = SEQUENCES[idx]
                    template = read_html_file("get.html")
                    # Renderizamos pasando el índice y la secuencia
                    content = template.render(context={"index": idx, "sequence": seq})
                    self.send_response_200(content)
                else:
                    self.send_error_page()

            # --- Ejercicio 3: GENE (/gene?name=X) ---
            elif path == "/gene":
                gene_name = params.get('name', [""])[0]
                gene_seq = genes.get(gene_name)

                if gene_seq:
                    template = read_html_file("gene.html")
                    content = template.render(context={"name": gene_name, "sequence": gene_seq})
                    self.send_response_200(content)
                else:
                    self.send_error_page()

            # --- Error: Recurso no encontrado ---
            else:
                self.send_error_page()

        except Exception as e:
            print(f"DEBUG Error: {e}")
            self.send_error_page()

    def send_response_200(self, content):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content.encode())

    def send_error_page(self):
        template = read_html_file("error.html")
        content = template.render()
        self.send_response(404)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(content.encode())


# --- Ejecución del servidor ---
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), SeqHandler) as httpd:
    print(f"Servidor activo en puerto {PORT}")
    httpd.serve_forever()