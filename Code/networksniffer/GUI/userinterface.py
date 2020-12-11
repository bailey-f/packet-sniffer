import tkinter as tk
from tkinter import *

class NavBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

class StatusBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        statusbar = Label(self, text="Status: 0", bd=1, relief=SUNKEN, anchor=W)
        statusbar.pack(side="bottom", fill="x")

class ToolBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.toolbar = Menu(self)
        self.parent.root.config(menu=self.toolbar)
        self.subMenu = Menu(self.toolbar, tearoff=0)
        self.toolbar.add_cascade(label='File', menu=self.subMenu)
    
    def add_command(self, name, func):
        self.subMenu.add_command(label=name, command=func)
        


class UserInterface(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("350x200")

        tk.Frame.__init__(self, self.root)
        self.statusbar = StatusBar(self)
        self.toolbar = ToolBar(self)
        self.navbar = NavBar(self)

        self.text = tk.Text(self.root, height=50, width=50)
        self.text.pack(side="left", fill="x")
        self.scroll_bar = tk.Scrollbar(self.root)

        self.scroll_bar.pack(side="right")
        self.statusbar.pack(side="bottom", fill="x")
        self.toolbar.pack(side="top", fill="x")
        self.navbar.pack(side="left", fill="y")
    
    def register_packet(self, packet):
        self.text.insert(tk.END, "\n----------| NEW PACKET |----------\n")
        self.text.insert(tk.END, "\nSource IP: " + str(packet.sourceIP))
        self.text.insert(tk.END, "\nDestination IP: " + str(packet.destIP))
        self.text.insert(tk.END, "\nVers: " + str(packet.vers))
        self.text.insert(tk.END, "\nProtocol: " + str(packet.protocol))
        self.text.insert(tk.END, "\nSource Port: " + str(packet.srcPort))
        self.text.insert(tk.END, "\nDestination Port: " + str(packet.destPort))
        self.text.insert(tk.END, "\nSequence Number: " + str(packet.seqNum))
        if(packet.protocol=="TCP"):
            self.text.insert(tk.END, "\nFlags: " + str(packet.flags))
        
        self.text.insert(tk.END, "\nPayload: \n" + str(packet.payload.data))
        self.text.insert(tk.END, "\n----------| END PACKET |----------\n")
        








    def add_toolbar_command(self, name, func):
        self.toolbar.add_command(name, func)

    def render(self):
        self.root.mainloop()
    
