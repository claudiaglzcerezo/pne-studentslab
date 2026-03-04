from Client0 import Client
PRACTICE = 2
EXERCISE = 1
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
IP = "212.128.255.99"
PORT = 8080

# -- Create a client object
c = Client(IP, PORT)

# -- Test the ping method
c.ping()
