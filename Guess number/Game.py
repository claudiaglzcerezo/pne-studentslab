import socket
import random
PORT = 8080
IP = "127.0.0.1"
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.listen()

class NumberGuesser:
    def __init__(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = []
    def guess(self, number):
        self.attempts.append(number)
        if number == self.secret_number:
            return f"You won after{len(sel.attempts)} attempts"
        elif number < self.secret_number:
            return "Higher"
        else:
            return "Lower"


while True:

    try:
        (cs, addr) = ls.accept()
        game = NumberGuesser()
    except KeyboardInterrupt:
        ls.close()
        exit()
    else:

        msg_raw = cs.recv(2048)
        msg = msg_raw.decode().strip().split(" ")

