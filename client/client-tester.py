import socket
import select
import json
import threading
# Set up the socket object


client_socket = socket.socket()

# Connect to the server
# Change to your server's address and port
server_address = ('localhost', 8000)
client_socket.connect(server_address)
client_socket.setblocking(0)


def receive():
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                continue
            print(message)
            # if the messages from the server is NAME send the client's name

        except socket.error:
            # an error will be printed on the command line or console if there's an error
            print(socket.error)
            break


def send():
    while True:
        message = input('Enter a message to send to the server: ')
        client_socket.send(message.encode())
        break


rcv = threading.Thread(target=receive())
snd = threading.Thread(target=send())
rcv.start()
snd.start()
