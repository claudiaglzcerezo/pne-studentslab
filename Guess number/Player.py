from Game import NumberGuesser
IP = "127.0.0.1"
PORT = 8080
c = NumberGuesser(IP, PORT)
number = c.guess(input("My guess is: "))