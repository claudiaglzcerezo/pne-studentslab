import socket
PORT = 8080
IP ="127.0.0.1"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((IP, PORT))
    print("Connected! Start guessing")
    game_over = False
    while not game_over:
        guess = input("Enter your guess: ")
        if guess:
            s.send(guess.encode())
            r = s.recv(2048).decode()
            print(f"Result: {r}")
            if "You won" in r:
                game_over = True
except ConnectionRefusedError:
    print("Server is down")