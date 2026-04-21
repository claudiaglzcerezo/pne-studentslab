from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import jinja2 as j
from pathlib import Path
import os

PORT = 8081

SEQUENCES = [
'GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAG',
'AAAAAAGGGGGGTTTTTTCCCCCCAAAAAAGGGGGGTTTTTTCCCCCCAAAAAAGGGGGGTTTTT',
'ATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCA',
'CCGGTTAACCGGTTAACCGGTTAACCGGTTAACCGGTTAACCGGTTAACCGGTTAACCGGTTAAC',
'GAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAGAG'
]
GENES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

# Jinja
env = j.Environment(loader=j.FileSystemLoader("html"))

def read_html_file(filename, context=None):
    template = env.get_template(filename)
    return template.render(context or {})


class SeqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        print(f"Requested path: {path}")


        if path == "/ping":
            html = read_html_file("ping.html")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())


        elif path == "/":
            html = read_html_file("index.html")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())


        elif path == "/get":
            query = parse_qs(parsed_path.query)
            if "n" in query:
                try:
                    n = int(query["n"][0])
                    if 0 <= n <= 4:
                        sequence = SEQUENCES[n]
                        html = read_html_file("get.html", {"sequence": sequence,"n": n})
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        self.wfile.write(html.encode())
                    else:
                        raise ValueError
                except:
                    self.send_error(400, "Invalid sequence number")
            else:
                self.send_error(400, "Missing parameter n")


        elif path == "/gene":
            query = parse_qs(parsed_path.query)
            if "g" in query:
                try:
                    g = query["g"][0]
                    if g in GENES:
                        file_path = os.path.join("sequences", f"{g}.txt")
                        with open(file_path, "r") as f:
                            sequence = "".join(line.strip()for line in f if not line.startswith(">"))

                        gene = "\n".join(sequence[i:i + 60] for i in range(0, len(sequence), 60))
                        html = read_html_file("gene.html", {"gene_name": g,"gene": gene})
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        self.wfile.write(html.encode())
                    else:
                        raise ValueError
                except:
                    self.send_error(400, "Not valid gene")
            else:
                self.send_error(400, "Missing parameter g")


        elif path == "/operation":
            query = parse_qs(parsed_path.query)
            if "seq" in query and "op" in query:
                seq = query["seq"][0].upper()
                op = query["op"][0]
                if not all(base in "ATCG" for base in seq):
                    html = read_html_file("error.html")
                    self.send_response(400)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(html.encode())
                    return
                try:
                    if op == "1":
                        total = len(seq)

                        countA = seq.count("A")
                        countC = seq.count("C")
                        countG = seq.count("G")
                        countT = seq.count("T")

                        result = (
                            f"Total length: {total}<br>"
                            f"A: {countA} ({countA / total * 100:.1f}%)<br>"
                            f"C: {countC} ({countC / total * 100:.1f}%)<br>"
                            f"G: {countG} ({countG / total * 100:.1f}%)<br>"
                            f"T: {countT} ({countT / total * 100:.1f}%)"
                        )
                    elif op == "2":
                        comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
                        result = "".join(comp[b] for b in seq)
                    elif op == "3":
                        result = seq[::-1]
                    else:
                        raise ValueError
                    html = read_html_file("operation.html", {"sequence": seq,"result": result,"operation": op})
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(html.encode())
                except:
                    self.send_error(400, "Invalid operation")
            else:
                self.send_error(400, "Missing parameters")


        else:
            html = read_html_file("error.html")
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

if __name__ == "__main__":
    server = HTTPServer(("", PORT), SeqHandler)
    print(f"Server running on http://localhost:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.server_close()