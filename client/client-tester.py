import socket
import select
import json
# Set up the socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
# Change to your server's address and port
server_address = ('localhost', 8000)
client_socket.connect(server_address)

while True:
    # Prompt the user to input a message
    message = input('Enter a message to send to the server: ')

    # Send the message to the server
    client_socket.sendall(message.encode())

    # Set response timeout
    client_socket.settimeout(3)

    # Receive the response from the server
    try:
        response = client_socket.recv(1024).decode()
        # Print out the response
        print(f'Received from server: {response}')
    except socket.timeout:
        print('The server did not respond in time')

    # Check if the user wants to exit
    if message.lower() == 'exit':
        break

# Close the socket
client_socket.close()
