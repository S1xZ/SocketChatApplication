# import all the required modules
import socket
import threading
import json
from tkinter import *
from tkinter import font
from tkinter import ttk

SERVER = 'localhost'
PORT = 8000
FORMAT = "utf-8"
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


class GUI:
    # constructor method
    def __init__(self):

        # Make root Window
        self.root = Tk()
        self.root.withdraw()

        # login window
        self.login = Toplevel()
        self.login.title("Chat App")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        # create a Label
        self.lbl_login = Label(self.login,
                               text="Please login to continue",
                               justify=CENTER,
                               font="Helvetica 14 bold")
        self.lbl_login.place(relheight=0.15, relx=0.2, rely=0.07)

        # create a Label
        self.lbl_login_name = Label(self.login,
                                    text="Name: ",
                                    font="Helvetica 12")
        self.lbl_login_name.place(relheight=0.2,
                                  relx=0.1,
                                  rely=0.2)

        # create a entry box for typing the message
        self.ent_username = Entry(self.login, font="Helvetica 14")
        self.ent_username.place(relwidth=0.4,
                                relheight=0.12,
                                relx=0.35,
                                rely=0.2)

        # set the focus to entry login
        self.ent_username.focus()

        # create a Continue Button
        self.btn_summit_username = Button(self.login,
                                          text="CONTINUE",
                                          font="Helvetica 14 bold",
                                          command=lambda: self.setUserName(self.ent_username.get()))
        self.btn_summit_username.place(relx=0.4,
                                       rely=0.55)

        # bind a key to call the same
        self.root.mainloop()

    def setUserName(self, username):
        # Destroy login window
        self.login.destroy()
        self.layout(username)

        # the thread to receive messages
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    # The main layout of the chat
    def layout(self, name):
        # set username
        self.name = name

        # to show chat window
        self.root.deiconify()
        self.root.title("CHATROOM")
        self.root.resizable(width=False,
                            height=False)
        self.root.configure(width=470,
                            height=550,
                            bg="#17202A")

        # create a Label
        self.lbl_head = Label(self.root,
                              bg="#ffe291",
                              fg="#000000",
                              text=self.name,
                              font="Helvetica 13 bold",
                              pady=5)

        self.lbl_head.place(relwidth=1)

        # create a Label
        self.lbl_line = Label(self.root,
                              width=450,
                              bg="#ABB2B9")

        self.lbl_line.place(relwidth=1,
                            rely=0.07,
                            relheight=0.012)

        # create a text box
        self.txt_message = Text(self.root,
                                width=20,
                                height=2,
                                bg="#ffcac4",
                                fg="#000000",
                                font="Helvetica 14",
                                padx=5,
                                pady=5)

        self.txt_message.place(relheight=0.745,
                               relwidth=1,
                               rely=0.08)
        self.txt_message.config(cursor="arrow")

        # create a Label
        self.lbl_bottom = Label(self.root,
                                bg="#ABB2B9",
                                height=80)

        self.lbl_bottom.place(relwidth=1,
                              rely=0.825)

        # create a entry box for typing the message
        self.ent_message = Entry(self.lbl_bottom,
                                 bg="#2C3E50",
                                 fg="#EAECEE",
                                 font="Helvetica 13")
        self.ent_message.place(relwidth=0.74,
                               relheight=0.06,
                               rely=0.008,
                               relx=0.011)

        # set the focus to entry
        self.ent_message.focus()

        # create a Send Button
        self.btn_message = Button(self.lbl_bottom,
                                  text="Send",
                                  font="Helvetica 10 bold",
                                  width=20,
                                  bg="#ABB2B9",
                                  command=lambda: self.handleSend(self.ent_message.get()))
        self.btn_message.place(relx=0.77,
                               rely=0.008,
                               relheight=0.06,
                               relwidth=0.22)

        # create a scroll bar
        scrollbar = Scrollbar(self.txt_message)
        scrollbar.place(relheight=1,
                        relx=0.974)
        scrollbar.config(command=self.txt_message.yview)

        # function to start the thread for sending messages
        self.txt_message.config(state=DISABLED)

    # function to start the thread for sending messages
    def handleSend(self, msg):
        self.txt_message.config(state=DISABLED)
        self.msg = msg
        self.ent_message.delete(0, END)
        send_thread = threading.Thread(target=self.send)
        send_thread.start()

    # function to receive server's messages
    def receive(self):
        client.send(json.dumps({
            "type": "username",
            "data": self.name
        }).encode())
        while True:
            try:
                responseJSON = client.recv(1024).decode()
                print(f'Received from server: {responseJSON}')
                responseObject = json.loads(responseJSON)
                print(f'Object from server: {responseObject}')
                if (responseObject["type"] == "direct_message"):
                    print(f'Received from server: {responseObject}')
                    # insert messages to text box
                    self.txt_message.config(state=NORMAL)
                    self.txt_message.insert(
                        END, responseObject["sender"]+" : "+responseObject["data"]+"\n\n")

                    self.txt_message.config(state=DISABLED)
                    self.txt_message.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occurred")
                client.close()
                break

    # function to send server's messages
    def send(self):
        self.txt_message.config(state=DISABLED)
        while True:
            message = json.dumps({
                "type": "direct_message",
                "recipient": "test",
                "data": self.msg
            })
            client.send(message.encode())
            break


# create a GUI class object
g = GUI()
