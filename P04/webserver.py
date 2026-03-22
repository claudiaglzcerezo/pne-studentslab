import socket
import termcolor


# -- Server network parameters
IP = "127.0.0.1"
PORT = 8080


def process_client(s):
    req_raw = s.recv(2000)
    req = req_raw.decode()
    # -- Split the request messages into lines
    lines = req.split('\n')
    req_line = lines[0]
    path = req_line.split('')[1]
    termcolor.cprint(f"Request: {req_line}", "green")
    paths = {"/info/A": "html/info/A.html", "/info/C": "html/info/C.html", "/info/G": "html/info/G.html", "/info/T": "html/info/T.html"}

    if path == paths:
        status = "HTTP/1.1200 Ok\n"
        file_to_open = paths[path]
    else:
        status = "HTTP/1.1404 Not Found\n"
        file_to_open = "html/error.html"
    with open(file_to_open, "r") as f:
        body = f.read()

    header = f"Content-Type: text/html\nContent-Lenght:{len(body)}\n\n"
    header += f"Content-Length: {len(body)}\n"
    cs.send((status + header + "\n" + body).encode())
# -------------- MAIN PROGRAM
# ------ Configure the server
# -- Listening socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# -- Setup up the socket's IP and PORT
ls.bind((IP, PORT))
# -- Become a listening socket
ls.listen()
while True:
    (cs, addr) = ls.accept()
    process_client(cs)
    cs.close()
