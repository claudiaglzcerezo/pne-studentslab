import socket
PORT = 8081
IP = "127.0.0.1"
MAX_OPEN_REQUESTS = 5
number_con = 0
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:

        print("Waiting for connections at {}, {} ".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

        number_con += 1

        print("CONNECTION: {}. From the IP: {}".format(number_con, address))

        msg = clientsocket.recv(2048).decode("utf-8")
        print("Message from client: {}".format(msg))

        m = "Hello from the teacher's server\n"
        send_bytes = str.encode(m)
                # We must write bytes, not a string
                clientsocket.send(send_bytes)
                clientsocket.close()

except socket.error:
    print("Problems using ip {} port {}. Is the IP correct? Do you have port permission?".format(IP, PORT))

except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()