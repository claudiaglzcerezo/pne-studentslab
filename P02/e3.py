from Client0 import Client
from S08.server import message

PRACTICE = 2
EXERCISE = 3
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
IP = "212.128.255.54"
PORT = 8081
c = Client(IP, PORT)
flag = True
while flag:
    message = input("Enter a message: ").lower()
    if message == "exit":
        flag = False
    else:
        print("Sending a message to the server...")
        response = c.talk("Testing!!!")
        print(f"Response: {response}")
