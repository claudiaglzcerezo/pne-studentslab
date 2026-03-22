import socket
import termcolor
IP = "127.0.0.1"
PORT = 8080
def process_client(cs):
    req = cs.recv(2000).decode()
    path = req.split('\n')[0].split('')[1]
    termcolor.cprint(f"Request: {path}", "green")
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
    cs.send((status + header + body).encode())

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.listen()
while True:
    (cs, addr) = ls.accept()
    process_client(cs)
    cs.close()