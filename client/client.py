# import all the required modules
import socket
import threading
import json
from datetime import datetime
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox

SERVER = '26.122.204.60'
PORT = 8000
FORMAT = "utf-8"
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


class GUI:
    # constructor method
    def __init__(self):
        # Program Variables
        self.isStart = True
        self.client_list = []
        self.client_chats = {}
        self.create_group_list = []
        self.join_group_list = []
        self.join_group_chats = {}
        self.username = "None"
        self.current_client_chat = "None"
        self.current_group_chat = "None"
        self.current_window = "login"
        self.is_group = False

        # Make root Window
        self.root = Tk()

        # Create Login Window
        self.create_root_window()
        self.create_home_window()
        self.create_login_window()
        # self.login.withdraw()
        self.home.withdraw()
        self.root.withdraw()

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
        self.ent_login_username = Entry(self.login, font="Helvetica 14")
        self.ent_login_username.place(relwidth=0.4,
                                      relheight=0.12,
                                      relx=0.35,
                                      rely=0.2)

        # set the focus to entry login
        self.ent_login_username.focus()

        # for error message
        self.lbl_login_error = Label(self.login,
                                     text="",
                                     justify=CENTER,
                                     fg="red",
                                     font="Helvetica 8 bold")
        # create a Continue Button
        self.btn_login_summit_username = Button(self.login,
                                                text="CONTINUE",
                                                font="Helvetica 14 bold",
                                                command=lambda: self.on_click("startup", type="username", data=self.ent_login_username.get()))
        self.btn_login_summit_username.place(relx=0.4,
                                             rely=0.55)

        self.login.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def create_home_window(self):
        # to show chat window
        self.home = Toplevel()
        self.home.title("CHAT APP")
        self.home.resizable(width=False,
                            height=False)
        self.home.geometry("400x300")

        # create a Label
        self.lbl_home_head = Label(self.home,
                                   text="Username : "+self.username,
                                   font="Helvetica 13 bold",
                                   pady=3)
        self.lbl_home_head.place(relwidth=1)

        # create a Label
        self.lbl_home = Label(self.home,
                              text="Select Chatroom",
                              justify=CENTER,
                              font="Helvetica 14 bold")
        self.lbl_home.place(relheight=0.15, relx=0.3, rely=0.07)

        # create a Label
        self.lbl_home_clients = Label(self.home,
                                      text="Clients : ",
                                      font="Helvetica 12")
        self.lbl_home_clients.place(relheight=0.2,
                                    relx=0.2,
                                    rely=0.2)

        # create client option frame
        self.frame_home_clients = Frame(
            self.home, width=100, height=100)
        self.frame_home_clients.place(relwidth=0.5, rely=0.2, relx=0.35)
        self.lbl_home_client_chat = Label(self.frame_home_clients,
                                          text="Select Client Room",
                                          font="Helvetica 10",
                                          pady=3)
        self.lbl_home_client_chat.pack()
        self.txt_client_var = StringVar(self.home)
        self.combobox_home_client = ttk.Combobox(self.frame_home_clients,
                                                 values=self.client_list, textvariable=self.txt_client_var, state='readonly', postcommand=lambda: self.change_is_group(False))
        self.combobox_home_client.pack(pady=5)

        # create a group Label
        self.lbl_home_groups = Label(self.home,
                                     text="Groups : ",
                                     font="Helvetica 12")
        self.lbl_home_groups.place(relheight=0.2,
                                   relx=0.2,
                                   rely=0.4)

        # create client option frame
        self.frame_home_groups = Frame(
            self.home, width=100, height=100)
        self.frame_home_groups.place(relwidth=0.5, rely=0.4, relx=0.35)
        self.lbl_home_group_chat = Label(self.frame_home_groups,
                                         text="Select Group Room",
                                         font="Helvetica 10",
                                         pady=3)
        self.lbl_home_group_chat.pack()
        self.txt_group_var = StringVar(self.home)
        self.combobox_home_group = ttk.Combobox(self.frame_home_groups,
                                                values=self.create_group_list, textvariable=self.txt_group_var, postcommand=lambda: self.change_is_group(True))
        self.combobox_home_group.pack(pady=5)

        # create a Continue Button
        self.btn_home_summit_enter = Button(self.home,
                                            text="ENTER",
                                            font="Helvetica 14 bold",
                                            command=lambda: self.on_click("startup", type="openchat"))
        self.btn_home_summit_enter.place(relx=0.4,
                                         rely=0.8)

        self.home.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def create_root_window(self):

        # to show chat window
        self.root.title("CHAT APP")
        self.root.resizable(width=False,
                            height=False)
        self.root.geometry("470x650")
        self.root.configure(bg="#17202A")

        # create a Label
        self.lbl_root_head = Label(self.root,
                                   bg="#292F3F",
                                   fg="#FFFFFF",
                                   text="Username : "+self.username,
                                   font="Helvetica 14 bold",
                                   pady=3,
                                   height=2)
        self.lbl_root_head.place(relwidth=1)

        self.lbl_root_sub_head = Label(self.root,
                                       bg="#292F3F",
                                       fg="#FFFFFF",
                                       text="Chat room with "+self.current_client_chat,
                                       font="Helvetica 12 bold",
                                       pady=3)
        self.lbl_root_sub_head.place(relwidth=1, rely=0.08)

        # Create button
        self.btn_root_back = Button(self.root,
                                    text="Back",
                                    font="Helvetica 13",
                                    command=lambda: self.on_click("startup", type="backtohome"))
        self.btn_root_back.place(relwidth=0.2, rely=0.02, relx=0.02)
        # create a text box
        self.txt_root_message = Text(self.root,
                                     height=2,
                                     width=20,
                                     bg="#373E4E",
                                     fg="#FFFFFF",
                                     font="Helvetica 13",
                                     padx=15,
                                     pady=15,
                                     cursor="arrow",
                                     state=DISABLED)
        self.txt_root_message.place(relheight=0.7,
                                    relwidth=0.9,
                                    relx=0.05,
                                    rely=0.126)

        # create a scroll bar
        scrollbar = Scrollbar(self.txt_root_message,
                              command=self.txt_root_message.yview)
        scrollbar.place(relheight=0.974,
                        relx=1.5)

        # create a Label
        self.lbl_root_bottom = Label(self.root,
                                     bg="#ABB2B9",
                                     height=80
                                     )
        self.lbl_root_bottom.place(relwidth=1, rely=0.85)

        # create a entry box for typing the message
        self.ent_root_message = Entry(self.lbl_root_bottom,
                                      bg="#2C3E50",
                                      fg="#EAECEE",
                                      font="Helvetica 13")
        self.ent_root_message.place(relwidth=0.74,
                                    relheight=0.06,
                                    rely=0.008,
                                    relx=0.011)
        self.ent_root_message.focus()

        # create a Send Button
        self.btn_root_message = Button(self.lbl_root_bottom,
                                       text="Send",
                                       font="Helvetica 10 bold",
                                       width=20,
                                       bg="#ABB2B9",
                                       command=lambda: self.on_click("sending", type="direct_message", data=self.ent_root_message.get()))
        self.btn_root_message.place(relx=0.77,
                                    rely=0.008,
                                    relheight=0.06,
                                    relwidth=0.22)

        # function to start the thread for sending messages
        self.txt_root_message.config(state=DISABLED)

        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

    # Handle On Window Close
    def on_window_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.isStart = False
            self.login.destroy()
            self.home.destroy()
            self.root.destroy()
            client.close()

    # Main method
    def on_click(self, action, type=None, data=None):
        if action == "startup":
            if type == 'username':
                self.handle_send_update_username(data)
            elif type == 'openchat':
                if self.is_group:
                    self.current_group_chat = self.combobox_home_group.get()
                else:
                    self.current_client_chat = self.combobox_home_client.get()
                self.handle_open_chat(self.is_group)
            elif type == 'backtohome':
                self.handle_back_to_home(self.is_group)
        elif action == "sending":
            self.handle_send_message(data, self.is_group)

    # handle send message to server
    def handle_send_update_username(self, username):
        self.username = username
        message = json.dumps({
            "type": "username",
            "data": username
        })
        client.send(message.encode())
        # Fill here
        self.lbl_root_head.config(text="Username : "+username)
        self.lbl_home_head.config(text="Username : "+username)
        self.username = username

    def handle_open_chat(self, is_group):
        # re-window the chat window
        self.home.withdraw()
        self.root.deiconify()

        # Attempt swap message
        if is_group:
            # Check that if group is existed
            if self.combobox_home_group.get() not in self.create_group_list:
                self.handle_send_create_group(self.combobox_home_group.get())
            # Check that if group is joined
            if self.combobox_home_group.get() not in self.join_group_list:
                self.handle_send_join_group(self.combobox_home_group.get())
            self.swap_stored_chat(self.current_group_chat,
                                  self.combobox_home_group.get(), True)
        else:
            self.swap_stored_chat(self.current_client_chat,
                                  self.combobox_home_client.get(), False)

    def handle_back_to_home(self, is_group):
        self.root.withdraw()
        self.txt_root_message.delete(END)
        if is_group:
            self.join_group_chats[self.current_group_chat] = self.txt_root_message.get(
                "1.0", 'end-1c')
            self.current_group_chat = None
        else:
            self.client_chats[self.current_client_chat] = self.txt_root_message.get(
                "1.0", 'end-1c')
            self.current_client_chat = None
        self.home.deiconify()

    def handle_send_message(self, message, is_group):
        if (is_group):
            self.handle_send_group_message(
                self.current_group_chat,  message)
        else:
            self.handle_send_direct_message(self.current_client_chat, message)

    def handle_send_direct_message(self, recipient, message):
        self.ent_root_message.delete(0, END)
        send_message = json.dumps({
            "type": "direct_message",
            "recipient": recipient,
            "data": message
        })
        client.send(send_message.encode())
        self.insert_message(self.username, message, True)

    def handle_send_create_group(self, group_name):
        message = json.dumps({
            "type": "create",
            "data": group_name
        })
        client.send(message.encode())

    def handle_send_join_group(self, group_name):
        self.join_group_chats[self.current_group_chat] = f"Welcome to {group_name}"+"\n\n"
        message = json.dumps({
            "type": "join",
            "data": group_name
        })
        client.send(message.encode())

    def handle_send_group_message(self, group_name, message):
        self.ent_root_message.delete(0, END)
        send_message = json.dumps({
            "type": "group_message",
            "group": group_name,
            "data": message
        })
        client.send(send_message.encode())
        self.insert_message(self.username, message, True)

    def on_receive(self, response_object):
        print(f'Object from server: {response_object}')
        respond_type = response_object["type"]
        if (respond_type == "users" or respond_type == "username"):
            self.handle_receive_update_username(response_object)
        elif respond_type == "direct_message":
            self.handle_receive_direct_message(response_object)
        elif respond_type == "group_message":
            self.handle_receive_group_message(response_object)
        elif respond_type == "groups":
            self.handle_receive_groups(response_object)

    # handle receive message from server
    def handle_receive_update_username(self, response_object):
        if (response_object["type"] == "username" and self.current_window == "login"):
            self.lbl_login_error.config(text="Error: Name already exist!")
            self.lbl_login_error.place(
                relx=0.35,
                rely=0.33)
            return
        # Set new client_list and create_group_list
        self.client_list = response_object["data"]
        self.create_group_list = response_object["group_data"]
        print("client_list : ", self.client_list)
        print("created_group : ", self.create_group_list)
        # Set Variable
        self.combobox_home_client.config(values=self.client_list)
        self.combobox_home_group.config(values=self.create_group_list)

        # Crate new chat for unexist chat
        for user in response_object["data"]:
            if (user not in self.client_chats):
                self.client_chats[user] = ""
        # Hide Login Window
        if (self.current_window == "login"):
            self.login.withdraw()
            self.home.deiconify()

    def handle_receive_direct_message(self, response_object):
        self.insert_message(
            response_object["sender"], response_object["data"])

    def handle_receive_group_message(self, response_object):
        print("Received group message", response_object)
        self.insert_message(
            response_object["sender"], response_object["data"], group_name=response_object["group"], is_group=True)

    def handle_receive_groups(self, response_object):
        if response_object["isExist"] and not response_object["isJoin"]:
            self.create_group_list = response_object["data"]
            print("created_group : ", self.create_group_list)
            self.combobox_home_group.config(values=self.create_group_list)

            # Crate new chat for unexist chat
            for group in response_object["data"]:
                if (group not in self.join_group_chats):
                    self.join_group_chats[group] = ""
        elif response_object["isExist"] and response_object["isJoin"]:
            self.join_group_list = response_object["data"]

    # Add message to text box

    def insert_message(self, sender, message, me=False, group_name="None", is_group=False):
        now = datetime.now().strftime("%H:%M:%S")
        # Create Message depends on is that myself
        if (me):
            message = now+" "+sender+"(me) : "+message+"\n\n"
        else:
            message = now+" "+sender+" : "+message+"\n\n"

        if is_group:
            if (group_name == self.current_group_chat) or me:
                self.txt_root_message.config(state=NORMAL)
                self.txt_root_message.insert(END, message)
                self.txt_root_message.config(state=DISABLED)
                self.txt_root_message.see(END)
                return
            self.join_group_chats[group_name] = self.join_group_chats[group_name] + message
            return
        # Insert Message to current text box
        if (sender == self.current_client_chat) or me:
            self.txt_root_message.config(state=NORMAL)
            self.txt_root_message.insert(END, message)
            self.txt_root_message.config(state=DISABLED)
            self.txt_root_message.see(END)
            return
        # Insert Message to stored chat
        self.client_chats[sender] = self.client_chats[sender] + message

    # Change Text Box
    def swap_stored_chat(self, old_recipient, new_recipient, is_group=False):
        # Insert new chat
        self.txt_root_message.config(state=NORMAL)
        self.txt_root_message.delete("1.0", END)
        if is_group:
            self.txt_root_message.insert(
                END,  self.join_group_chats[new_recipient])
        else:
            self.txt_root_message.insert(
                END,  self.client_chats[new_recipient])
        self.txt_root_message.config(state=DISABLED)
        self.txt_root_message.see(END)
        # Set current chat and sub text
        if is_group:
            self.current_group_chat = new_recipient
            self.lbl_root_sub_head.config(
                text="G."+self.current_group_chat+" Chat room")
        else:
            self.current_client_chat = new_recipient
            self.lbl_root_sub_head.config(
                text="Chat room with "+new_recipient)

    def change_is_group(self, is_group):
        self.is_group = is_group

    # thread function
    def receive(self):
        while self.isStart:
            try:
                responseJSON = client.recv(1024).decode()
                self.on_receive(json.loads(responseJSON))

            except Exception as e:
                # an error will be printed on the command line or console if there's an error
                print("Error has occured", e)
                break

    # End Class


# create a GUI class object
app = GUI()
