from Client0 import Client
from Seq2 import Seq

PRACTICE = 2
EXERCISE = 4
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
IP = "212.128.254.54"
PORT = 8080
c = Client(IP, PORT)
gen_list = ["FRAT1", "U5", "ADA", "FXN", "RNU6_269P"]
for gene in gen_list:
    s = Seq()
    filename = gene + ".txt"
    print(f"Loading {filename}...")
    s.read_fasta(filename)
    print(f"To Server: Sending {gene} Gene to server")
    response = c.talk(f"Sending {gene} Gene to server")
    print(f"From Server: {response}")
    sequence = str(s)
    print(f"To server: {sequence}")
    response = c.talk(sequence)
    print(f"From Server: {response}")