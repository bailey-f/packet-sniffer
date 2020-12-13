import tkinter as tk
from tkinter import *

class NavBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

class PacketFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        
        self.packetframe = Frame(self, bg="black", width=800, height=500)
        self.packetframe.pack(side="left", fill="both", padx=2, pady=2)
        self.packetframe2 = Frame(self.packetframe, bg="lightgrey", width=800, height=500, pady=2, padx=2)
        self.packetframe2.pack(side="left", fill="both", padx=2, pady=2, expand=True)
        self.h_number = Label(self.packetframe2, bg="white", cursor="dot", text="Number:", font=("roboto", 12), borderwidth=2, relief="groove")
        self.h_number.grid(column=0, row=0)
        self.h_src = Label(self.packetframe2, bg="white", cursor="dot", text="Source:", font=("roboto", 12), borderwidth=2, relief="groove")
        self.h_src.grid(column=1, row=0, columnspan=5)
        self.h_dest = Label(self.packetframe2, bg="white", cursor="dot", text="Destination:", font=("roboto", 12), borderwidth=2, relief="groove")
        self.h_dest.grid(column=6, row=0, columnspan=5)
        self.h_proto = Label(self.packetframe2, bg="white", cursor="dot", text="Protocol:", font=("roboto", 12), borderwidth=2, relief="groove")
        self.h_proto.grid(column=11, row=0)
        self.h_len = Label(self.packetframe2, bg="white", cursor="dot", text="Length:", font=("roboto", 12), borderwidth=2, relief="groove")
        self.h_len.grid(column=12, row=0, columnspan=1)
        self.h_info = Label(self.packetframe2, bg="white", cursor="dot", text="Info:", font=("roboto", 12), borderwidth=2, relief="groove")
        self.h_info.grid(column=13, row=0)

class DataFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.dataframe = Frame(self, bg="black", width=800, height=300)
        self.dataframe.pack(side="bottom", fill="both", padx=2, pady=2)
        self.dataframe2 = Frame(self.dataframe, bg="lightgrey", width=800, height=300, pady=2, padx=2)
        self.dataframe2.pack(side="bottom", fill="both", padx=2, pady=2, expand=True)
        
class StatusBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.statusbar = Label(self, text="Status: Doing nothing...", bd=1,
         relief=SUNKEN, anchor=W, width=1080)
        self.statusbar.pack(side=BOTTOM)
        self.pack(side=BOTTOM)
        
    def change_status(self, status):
        self.statusbar.config(text=str(status))

class ToolBar():
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.toolbar = Menu(self.parent)
        self.parent.config(menu=self.toolbar)
        self.subMenu = Menu(self.toolbar, tearoff=0)
        self.toolbar.add_cascade(label='File', menu=self.subMenu)
    
    def add_command(self, name, func):
        self.subMenu.add_command(label=name, command=func)
        


class UserInterface(tk.Tk):
    def __init__(self):
        super().__init__(screenName="Packet Sniffer")
        self.geometry("1080x720")
        self.state('zoomed')
        self.title('Packet Sniffer')
        self.toolbar = ToolBar(self)
        self.statusbar = StatusBar(self)
        self.dataframe = DataFrame(self)
        self.packetframe = PacketFrame(self)

        self.dataframe.pack(side="bottom", fill="both", padx=2, pady=2, expand=True)
        self.packetframe.pack(side="left", fill="both", padx=2, pady=2, expand=True)
       
        """    
        self.dataframe = FrameController(self, bg="black", width=800, height=300)
        self.dataframe.pack(side="bottom", fill="both", padx=2, pady=2)
        self.dataframe2 = FrameController(self.dataframe, bg="lightgrey", width=800, height=300, pady=2, padx=2)
        self.dataframe2.pack(side="bottom", fill="both", padx=2, pady=2, expand=True)
        """
        """
        self.packetframe = FrameController(self, bg="black", width=800, height=500)
        self.packetframe.pack(side="left", fill="both", padx=2, pady=2)
        self.packetframe2 = FrameController(self.packetframe, bg="lightgrey", width=800, height=500, pady=2, padx=2)
        self.packetframe2.pack(side="left", fill="both", padx=2, pady=2, expand=True)
        self.h_number = Label(self.packetframe2, bg="white", cursor="dot", text="Number:", font=("roboto", 12), borderwidth=2, relief="groove")
        self.h_number.grid(column=0, row=0)
        self.h_src = Label(self.packetframe2, bg="white", cursor="dot", text="Source:", font=("roboto", 12), borderwidth=2, relief="groove")
        self.h_src.grid(column=1, row=0, columnspan=5)
        self.h_dest = Label(self.packetframe2, bg="white", cursor="dot", text="Destination:", font=("roboto", 12), borderwidth=2, relief="groove")
        self.h_dest.grid(column=6, row=0, columnspan=5)
        self.h_proto = Label(self.packetframe2, bg="white", cursor="dot", text="Protocol:", font=("roboto", 12), borderwidth=2, relief="groove")
        self.h_proto.grid(column=11, row=0)
        self.h_len = Label(self.packetframe2, bg="white", cursor="dot", text="Length:", font=("roboto", 12), borderwidth=2, relief="groove")
        self.h_len.grid(column=12, row=0, columnspan=1)
        self.h_info = Label(self.packetframe2, bg="white", cursor="dot", text="Info:", font=("roboto", 12), borderwidth=2, relief="groove")
        self.h_info.grid(column=13, row=0)
        """


    
    def register_packet(self, packet):
        self.statusbar.change_status("Status: Capturing Packets...")

        self.statusbar.change_status("Status: Doing nothing...")
        

    def add_toolbar_command(self, name, func):
        self.toolbar.add_command(name, func)

    def render(self):
        self.mainloop()
    
