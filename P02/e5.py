from Client0 import Client
from Seq2 import Seq
from e3 import response

PRACTICE = 2
EXERCISE = 5
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
IP = "212.128.254.54"
PORT = 8080
c = Client(IP, PORT)
s = Seq()
s.read_fasta("FRAT1.txt")
sequence = str(s)
print(f"Gene FRAT1: {sequence[:100]}...")
fragments = []
for i in range(5):
    start = i * 10
    end = start + 10
    fragment = sequence[start: end]
    fragments.append(fragment)
print(f"Sending  fragments to the server")
response = c.talk("Sending FRAT1 Gene to the server, in fragments of 10 bases")
print(f"Response: {response}")
for i, fragment in enumerate(fragments):
    fragment_msg = f"Fragment {i + 1}: {fragment}"
    print(fragment_msg)
    response = c.talk(fragment_msg)
    print(f"Response: {response}")
print("Process finished")