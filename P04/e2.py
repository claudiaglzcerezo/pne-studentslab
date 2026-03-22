import socket
import termcolor
IP = "127.0.0.1"
PORT = 8080
def process_client(cs):
    req = cs.recv(2000).decode()
    path = req.split('\n')[0].split('')[1]
    termcolor.cprint(f"Request: {path}", "green")
    if path == "/info/A":
        with open("html/info/A.html", "r") as f:
            body = f.read()
    else:
        body = ""
    header = f"HTTP/1.1200 Ok\nContent-Type: text/html\nContent-Lenght:{len(body)}\n\n"
    cs.send((header + body).encode())

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.listen()
while True:
    (cs, addr) = ls.accept()
    process_client(cs)
    cs.close()

