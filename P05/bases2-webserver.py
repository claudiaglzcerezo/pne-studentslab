import http.server
import socketserver
import os  # Importamos 'os' para poder comprobar si los archivos existen

# Define the Server's port
PORT = 8080

# This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        print(f"GET received! Request line: {self.requestline}")
        print(f" Path requested: {self.path}")

        if self.path == "/" or self.path == "/index.html":
            # Si piden la raíz o explícitamente el index, la ruta es html/index.html
            filepath = "html/index.html"
        else:
            # Para cualquier otra cosa (ej: /info/A.html), le añadimos "html" delante
            filepath = "html" + self.path

        # 2. Para cmprobar si el archivo solicitado existe en nuestro disco
        if os.path.exists(filepath) and os.path.isfile(filepath):
            # --- EL ARCHIVO EXISTE ---
            status_code = 200
            file_to_open = filepath
        else:
            # Por si piden algo raro (ej: /info/Z.html), servimos la página de error
            print(f" Warning: File {filepath} not found. Serving error.html")
            status_code = 404  # For Not Found
            file_to_open = "html/error.html"

        try:
            with open(file_to_open, "r", encoding="utf-8") as f:
                contents = f.read()

            self.send_response(status_code)

            # headers
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', str(len(contents.encode())))
            self.end_headers()
            self.wfile.write(contents.encode())

        except Exception as e:
            print(f"Internal server error: {e}")
            self.send_response(500)
            self.end_headers()


# handler
Handler = TestHandler

#socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    #Attender
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()