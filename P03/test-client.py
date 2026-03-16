from Client0 import Client

IP = "127.0.0.1"
PORT = 8080

print("-----| Practice 3, Exercise 7 |------")
print(f"Connection to SERVER at {IP}, PORT: {PORT}")

c = Client(IP, PORT)

print("* Testing PING...")
response = c.talk("PING")
print(response)

print("* Testing GET...")
seq0 = ""
for i in range(5):
    response = c.talk(f"GET {i}").strip()
    print(f"GET {i}: {response}")
    if i == 0:
        seq0 = response
print()

print("* Testing INFO...")
response = c.talk(f"INFO {seq0}")
print(response)

print("* Testing COMP...")
print(f"COMP {seq0}")
response = c.talk(f"COMP {seq0}")
print(response)

print("* Testing REV...")
print(f"REV {seq0}")
response = c.talk(f"REV {seq0}")
print(response)

print("* Testing GENE...")
genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]
for g in genes:
    print(f"GENE {g}")
    response = c.talk(f"GENE {g}")
    print(response))