import socket
from Seq1 import Seq

PORT = 8080
IP = "127.0.0.1"

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind((IP, PORT))
ls.listen()

print("SEQ Server configured!")

lst = ["ACGTG", "TGTGCC", "ACTGC", "ACCG", "AAAT"]

while True:
    print("Waiting for Clients...")
    try:
        (cs, client_ip_port) = ls.accept()
    except KeyboardInterrupt:
        ls.close()
        exit()
    else:
        msg_raw = cs.recv(2048)
        msg = msg_raw.decode().strip().split(" ")
        command = msg[0]

        if command == "PING":
            print(f"{command} connected!")
            response = "OK!" + "\n"
            cs.send(response.encode())
            cs.close()

        elif command == "GET":
            num = msg[1]
            n = int(num)
            if 0 <= n <= 4:
                print(f"{command}")
                response = lst[n] + "\n"
                print(lst[n])
                cs.send(response.encode())
                cs.close()
            else:
                print(f"{msg}")
                response = "NOT AN OPTION"
                cs.send(response.encode())
                cs.close()

        elif command == "INFO":
            seq = msg[1].strip()
            s = Seq(seq)
            total = len(seq)

            a = s.count_base("A")
            c = s.count_base("C")
            g = s.count_base("G")
            t = s.count_base("T")

            print(f"{command}")
            print("New sequence created!")

            # Formato de respuesta con porcentajes
            l = f"sequence {s}\n" + f"Total length: {total}\n" + \
                f"A: {a} ({a / total * 100:.1f}%)\n" + \
                f"C: {c} ({c / total * 100:.1f}%)\n" + \
                f"G: {g} ({g / total * 100:.1f}%)\n" + \
                f"T: {t} ({t / total * 100:.1f}%)\n"
            print(l)
            response = l
            cs.send(response.encode())
            cs.close()

        elif command == "COMP":
            seq = msg[1].strip()
            s = Seq(seq)
            c = s.complement()
            print(f"{command}")
            print("New sequence created!")
            print(f"{c}")
            response = c + "\n"
            cs.send(response.encode())
            cs.close()

        elif command == "REV":
            seq = msg[1].strip()
            s = Seq(seq)
            c = s.reverse()
            print(f"{command}")
            print("New sequence created!")
            print(f"{c}")
            response = c + "\n"
            cs.send(response.encode())
            cs.close()

        elif command == "GENE":
            gene = msg[1].strip()

            # Rutas para los archivos FASTA
            head = "../P00/S04/sequences/"
            tail = ".txt"

            print(f"{command}")

            s = Seq()
            s.read_fasta(head + gene + tail)
            print(str(s))
            response = str(s) + "\n"
            cs.send(response.encode())
            cs.close()