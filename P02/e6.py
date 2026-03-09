from Client0 import Client
from Seq2 import Seq

PRACTICE = 2
EXERCISE = 6
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
IP = "127.0.0.1"
PORT1 = 8080
PORT2 = 8081
c1 = Client(IP, PORT1)
c2 = Client(IP, PORT2)
s = Seq()
s.read_fasta("FRAT1.txt")
sequence = str(s)
print(f"Gene FRAT1: {sequence[:100]}...")
print("NULL Seq created")
fragments = []
for i in range(10):
    start = i * 10
    end = start + 10
    fragment = sequence[start: end]
    fragments.append(fragment)
print(f"Sending  fragments to the server")

for i, fragment in enumerate(fragments, 1):
    print(f"Fragment {i}: {fragment}")

response1 = c1.talk("Sending FRAT1 Gene to the server, in fragments of 10 bases")
response2 = c2.talk("Sending FRAT1 Gene to the server, in fragments of 10 bases")
print(f"Response: {response1}")
print(f"Response: {response2}")
for i, fragment in enumerate(fragments, 1):
    fragment_msg = f"Fragment {i + 1}: {fragment}"
    if i % 2 == 1:
        response1 = c1.talk(fragment_msg)
        print(f"Response: {response1}")
    else:
        response2 = c2.talk(fragment_msg)
        print(f"Response: {response2}")
print("Process finished")