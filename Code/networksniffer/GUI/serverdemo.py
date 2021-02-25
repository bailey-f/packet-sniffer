import socket
import struct
import threading
import datetime
from tkinter import *

class userInterface():
    def __init__(self):
        pass

    def start(self, main):
        self.usr_message = StringVar()
        self.sdframe_outer=Frame(main.ui.controlframe.server_win, bg="grey")
        self.sdframe_outer.pack(side="left", fill="both", padx=2, pady=2)
        self.sdframe_inner=Frame(
        self.sdframe_outer, bg="white", pady=2, padx=2, height=800, width=500, bd=0)
        self.sdframe_inner.grid(row=0, column=0, pady=2, padx=2)
        self.sdframe_outer.pack_propagate(0)
        self.sdframe_inner.grid_propagate(0)

        self.servercl_frame=Frame(
        self.sdframe_inner, bg="white", relief="flat", height=400, width=500, bd=2)
        self.clientcl_frame=Frame(
        self.sdframe_inner, bg="white", relief="flat", height=400, width=500, bd=2)
        self.servercl_frame.pack(side="top", fill="both", padx=2, pady=2)
        self.servercl_frame.pack_propagate(0)
        self.servercl_frame.update_idletasks()
        self.clientcl_frame.pack(side="bottom", fill="both", padx=2, pady=2)
        self.clientcl_frame.pack_propagate(0)
        self.clientcl_frame.update_idletasks()

        self.servercl_subframe1=Frame(
        self.servercl_frame, bg="grey", relief="flat", height=400, width=502, bd=2)
        self.servercl_servertitle=Frame(
        self.servercl_subframe1, bg="lightgrey", relief="flat", height=40, width=502, bd=2)
        self.servercl_subframe3=Frame(
        self.servercl_subframe1, bg="white", relief="flat", height=360, width=502, bd=2)
        self.servercl_subframe1.pack(side="top", fill="both", padx=2, pady=2)
        self.servercl_servertitle.pack(side="top", fill="both", padx=2, pady=2)
        self.servercl_subframe3.pack(side="top", fill="both", padx=2, pady=2)
        self.servercl_subframe1.pack_propagate(0)
        self.servercl_servertitle.pack_propagate(0)
        self.servercl_subframe3.pack_propagate(0)

        self.servertitle_lab=Label(self.servercl_servertitle, bg="lightgrey", cursor="dot",
                                    text="Server Side", font=("roboto", 12), borderwidth=2, relief="flat", anchor="center")
        self.servertitle_lab.pack(side="top", padx=2, pady=2)

        self.clientcl_subframe1=Frame(
        self.clientcl_frame, bg="grey", relief="flat", height=400, width=502, bd=2)
        self.clientcl_clienttitle=Frame(
        self.clientcl_subframe1, bg="lightgrey", relief="flat", height=40, width=502, bd=2)
        self.clientcl_subframe3=Frame(
        self.clientcl_subframe1, bg="white", relief="flat", height=300, width=502, bd=2)
        self.clientcl_subframe1.pack(side="top", fill="both", padx=2, pady=2)
        self.clientcl_clienttitle.pack(side="top", fill="both", padx=2, pady=2)
        self.clientcl_subframe3.pack(side="top", fill="both", padx=2, pady=2)
        self.clientcl_subframe1.pack_propagate(0)
        self.clientcl_clienttitle.pack_propagate(0)
        self.clientcl_subframe3.pack_propagate(0)

        self.clienttitle_lab=Label(self.clientcl_clienttitle, bg="lightgrey", cursor="dot",
                                    text="Client Side", font=("roboto", 12), borderwidth=2, relief="flat", anchor="center")
        self.clienttitle_lab.pack(side="top", padx=2, pady=2)

        self.clientcl_chatframe=Frame(
        self.clientcl_subframe1, bg="white", relief="flat", height=80, width=502, bd=2)
        self.clientcl_chatframe.pack(side="bottom", fill="both", padx=2, pady=2)
        self.clienttitle_lab=Entry(self.clientcl_chatframe, bg="lightgrey", width="45",
                                    font=("roboto", 12), borderwidth=2, relief="flat", textvariable=self.usr_message)
        self.clienttitle_lab.pack(side="left", padx=2, pady=2)
        self.clientcl_chatframe_butt = Button(self.clientcl_chatframe, text="Submit", font=("roboto", 12), borderwidth=0, relief="flat", anchor="center", activebackground="lightblue", highlightcolor="lightblue", background="white",
                                command=lambda: self.onClick(self.clientcl_chatframe_butt))
        self.clientcl_chatframe_butt.pack(side="right", padx=2, pady=2)

        self.server_text=Text(self.servercl_subframe3, bg="white", relief="flat",
                             padx=2, width=80, height=16, selectbackground="lightgreen")
        self.client_text=Text(self.clientcl_subframe3, bg="white", relief="flat",
                                 pady=2, padx=2, width=78, height=16, selectbackground="lightgreen")
        self.server_text.pack(side="bottom", fill="both", padx=2, pady=2)
        self.client_text.pack(side="top", fill="both", padx=2, pady=2)
        self.client_text.config(state=DISABLED)
        self.server_text.config(state=DISABLED)


        self.running = True
        self.server = Server(self)
        self.client = Client()
        threading.Thread(target=self._loop).start()
    
    def _loop(self):
        self.server.start()


    def onHover(self, button):
        if(button['bg'] == "lightgreen"):
            button['activebackground']="lightgreen"
            button.bind("<Leave>", func=lambda e: button.config(
                background="lightgreen"))
            button.bind("<Enter>", func=lambda e: button.config(
                background="lightblue"))
        elif(button['bg'] == "white"):
            button['activebackground']="white"
            button.bind("<Leave>", func=lambda e: button.config(
                background="white"))
            button.bind("<Enter>", func=lambda e: button.config(
                background="lightblue"))

    def onClick(self, button):
        self.onHover(button)
        if(button['text'] == "Submit"):
            self.submit()

        self.onHover(button)
        # actually load data

    def submit(self):
        usr_message = self.usr_message.get()
        print("message sent: " + usr_message)
        self.client_text.config(state=NORMAL)
        self.client_text.delete(1.0, "end")
        self.client_text.insert(1.0, (datetime.datetime.now().timestamp(), " | Client sent message: ", usr_message))
        self.client_text.config(state=DISABLED)
        self.client.client_socket.send(usr_message.encode())
        self.usr_message.set("")

class Server():
    def __init__(self, userinterface):
        self.ui = userinterface
        print(socket.gethostbyname(socket.gethostname()))
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 7789
        self.running = False
        self.server_socket = socket.socket()
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)

    def start(self):
        self.running = True
        threading.Thread(target=self._loop).start()
    
    def stop(self):
        self.running = False

    def _loop(self):
        conn, address = self.server_socket.accept()
        print("Connection from: " + str(address))
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            self.ui.server_text.config(state=NORMAL)
            self.ui.server_text.delete(1.0, "end")
            self.ui.server_text.insert(1.0, (datetime.datetime.now().timestamp(), " | Server recieved message: ", data))
            self.ui.server_text.config(state=DISABLED)
            print("from connected user: " + str(data))
        conn.close() 

class Client():
    def __init__(self, host=socket.gethostbyname(socket.gethostname()), apply=None):
        print(socket.gethostbyname(socket.gethostname()))
        self.host = host
        self.port = 7789
        self.running = False
        self.client_socket = socket.socket()
        self.client_socket.connect((self.host, self.port))


