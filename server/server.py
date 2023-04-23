import socket
import threading
import json


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}
        self.chat_groups = {}

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}...")

        while True:
            client_socket, client_address = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle_client, args=(client_socket, ))
            client_thread.start()
            print(f"Total Client: {threading.active_count() - 1}\n")

    def handle_client(self, socket):
        client_address = socket.getpeername()
        print(f"New client connected: {client_address}")
        nickname = None

        while True:
            message = socket.recv(1024).decode()
            if not message:
                break

            message = json.loads(message)
            print(message)
            # The client can set a nickname.
            # Each client can see a list of all clients.
            if message["type"] == "username":
                nickname = message["data"]

                if nickname in self.clients:
                    socket.send(json.dumps({
                        "type": "username",
                        "isExist": True,
                    }).encode())
                    continue

                self.clients[nickname] = socket
                print(f"Client {nickname} connected")
                self.update_users()

            # Each client can create a chat group(s) and join the chat group(s).
            # Each client can see a list of all created chat groups.
            elif message["type"] == "join":
                group_name = message["data"]

                if group_name not in self.chat_groups:
                    self.update_groups(isExist=False, isJoin=True)
                    continue

                self.chat_groups[group_name].append(socket)
                print(f"Client {nickname} joined group {group_name}")
                self.update_groups(isExist=True, isJoin=True)

            # Each client can create a chat group(s) and join the chat group(s).
            elif message["type"] == "create":
                group_name = message["data"]
                if group_name not in self.chat_groups:
                    self.chat_groups[group_name] = [socket]
                else:
                    self.update_groups(isExist=False, isJoin=False)
                    continue

                print(f"Client {nickname} created group {group_name}")
                self.update_groups(isExist=True, isJoin=False)

            # Each client can send a message to a chat group.
            elif message["type"] == "group_message":
                group_name = message["group"]
                message = message["data"]
                print(
                    f"Client {nickname} sent message to group {group_name}: {message}")
                self.send_group_message(group_name, nickname, socket, message)

            # Each client can send a direct message to other clients in the list.
            elif message["type"] == "direct_message":
                recipient = message["recipient"]
                message = message["data"]
                print(
                    f"Client {nickname} sent message to {recipient}: {message}")
                self.send_direct_message(recipient, nickname, message)

    def send_group_message(self, group_name, sender, sender_socket, message):
        for socket in self.clients:
            if self.clients[socket] in self.chat_groups[group_name] and socket != sender_socket:
                socket.send(json.dumps({
                    "type": "group_message",
                    "group": group_name,
                    "sender": sender,
                    "data": message
                }).encode())

    def send_direct_message(self, recipient, sender, message):
        for socket in self.clients:
            if self.clients[socket] == recipient:
                socket.send(json.dumps({
                    "type": "direct_message",
                    "sender": sender,
                    "data": message
                }).encode())

    def update_users(self):
        for socket in self.clients:
            socket.send(json.dumps({
                "type": "users",
                "data": list(self.clients.values())
            }).encode())

    def update_groups(self, isExist=False, isJoin=False):
        for socket in self.clients:
            socket.send(json.dumps({
                "type": "groups",
                "isExist": isExist,
                "isJoin": isJoin,
                "data": list(self.chat_groups.keys())
            }).encode())


if __name__ == "__main__":
    server = ChatServer("localhost", 8000)
    server.start()
