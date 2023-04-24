# import all the required modules
import socket
import threading
import json
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox

SERVER = 'localhost'
PORT = 8000
FORMAT = "utf-8"
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


class GUI:
    # constructor method
    def __init__(self):
        # Program Logic
        self.isStart = True

        # Make root Window
        self.root = Tk()
        self.root.withdraw()

        # Create Login Window
        self.create_login_window()

        # on closing the window
        self.login.protocol("WM_DELETE_WINDOW", self.on_login_window_close)
        self.root.protocol("WM_DELETE_WINDOW", self.on_root_window_close)

        # start receive thread message
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

        # bind a key to call the same
        self.root.mainloop()

    # Init Window
    def create_login_window(self):
        # login window
        self.login = Toplevel()
        self.login.title("CHAT APP")
        self.login.resizable(width=False, height=False)
        self.login.geometry("400x300")
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

        # for error message
        self.lbl_error = Label(self.login,
                               text="Error: Name already exist!",
                               justify=CENTER,
                               fg="red",
                               font="Helvetica 8 bold")
        # create a Continue Button
        self.btn_summit_username = Button(self.login,
                                          text="CONTINUE",
                                          font="Helvetica 14 bold",
                                          command=lambda: self.on_click("sending", type="username", data=self.ent_username.get()))
        self.btn_summit_username.place(relx=0.4,
                                       rely=0.55)

    def create_root_window(self):

        # to show chat window
        self.root.deiconify()
        self.root.title("CHAT APP")
        self.root.resizable(width=False,
                            height=False)
        self.root.geometry("470x550")
        self.root.configure(bg="#17202A")

        # create a Label
        self.lbl_head = Label(self.root,
                              bg="#ffe291",
                              fg="#000000",
                              text=self.username,
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
        self.ent_message.focus()

        # create a Send Button
        self.btn_message = Button(self.lbl_bottom,
                                  text="Send",
                                  font="Helvetica 10 bold",
                                  width=20,
                                  bg="#ABB2B9",
                                  command=lambda: self.on_click("sending", type="direct_message", data=self.ent_message.get()))
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

    # Handle On Window Close
    def on_login_window_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.isStart = False
            self.login.destroy()
            self.root.destroy()
            client.close()

    def on_root_window_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.isStart = False
            self.root.destroy()
            client.close()

    # Main method
    def on_click(self, action, type=None, data=None):
        if action == "sending":
            if type == 'username':
                self.handle_send_update_username(data)

            elif type == "direct_message":
                self.handle_send_direct_message(data)

    def handle_send_update_username(self, username):
        self.username = username
        message = json.dumps({
            "type": "username",
            "data": username
        })
        client.send(message.encode())

    def handle_send_direct_message(self, message):
        self.txt_message.config(state=DISABLED)
        self.ent_message.delete(0, END)
        self.txt_message.config(state=DISABLED)
        message = json.dumps({
            "type": "direct_message",
            "recipient": "test",
            "data": message
        })
        client.send(message.encode())

    def on_receive(self, response_object):
        print(f'Object from server: {response_object}')
        if (response_object["type"] == "users" or response_object["type"] == "username"):
            self.handle_receive_update_username(response_object)
        elif response_object["type"] == "direct_message":
            self.handle_receive_direct_message(response_object)

    def handle_receive_update_username(self, response_object):
        if (response_object["type"] == "username"):
            self.lbl_error.place(
                relx=0.35,
                rely=0.33)
            return
        self.login.destroy()
        self.create_root_window()

    def handle_receive_direct_message(self, response_object):
        # insert messages to text box
        self.txt_message.config(state=NORMAL)
        self.txt_message.insert(
            END, response_object["sender"]+" : "+response_object["data"]+"\n\n")

        self.txt_message.config(state=DISABLED)
        self.txt_message.see(END)

    # thread function
    def receive(self):
        while self.isStart:
            try:
                responseJSON = client.recv(1024).decode()
                self.on_receive(json.loads(responseJSON))

            except Exception as e:
                # an error will be printed on the command line or console if there's an error
                print(e)
                break

    # End Class


# create a GUI class object
app = GUI()
