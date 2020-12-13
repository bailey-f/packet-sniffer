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
        self.packetcount = 0

        
        # make the outer packet frame, then make the inner packet frame to hold the headers
        self.packetframe = Frame(self, bg="grey", width=800, height=500)
        self.packetframe.pack(side="left", fill="y", padx=2, pady=2)
        self.packetframe2 = Frame(self.packetframe, bg="lightgrey", width=800, height=500, pady=2, padx=2)
        self.packetframe2.pack(side="left", fill="both", padx=2, pady=2)
        # make the canvas & scrollbar for where we are holding our packets
        self.packetrows = Canvas(self.packetframe2, bg="lightgrey", width=800, height=500, relief="flat")
        self.vsb = Scrollbar(self.packetframe2, orient="vertical", command=self.packetrows.yview)
        self.vsb.grid(row=0, column=16, sticky="ns")
        self.packetrows.configure(yscrollcommand=self.vsb.set)
        self.packetrows.config(scrollregion=self.packetrows.bbox("all"))
        self.packetrows.grid(row=0, column=0, sticky="news", pady=2, padx=2)

        # make the headers
        self.h_number = Label(self.packetrows, bg="lightgrey", cursor="dot", text="Number", font=("roboto", 12), borderwidth=2, relief="flat")
        self.h_number.grid(column=0, row=0, columnspan=1)
        self.h_src = Label(self.packetrows, bg="lightgrey", cursor="dot", text="     Source     ", font=("roboto", 12), borderwidth=2, relief="flat")
        self.h_src.grid(column=1, row=0)
        self.h_dest = Label(self.packetrows, bg="lightgrey", cursor="dot", text="     Destination     ", font=("roboto", 12), borderwidth=2, relief="flat")
        self.h_dest.grid(column=6, row=0)
        self.h_proto = Label(self.packetrows, bg="lightgrey", cursor="dot", text="Protocol", font=("roboto", 12), borderwidth=2, relief="flat")
        self.h_proto.grid(column=11, row=0, columnspan=1)
        self.h_len = Label(self.packetrows, bg="lightgrey", cursor="dot", text="Length", font=("roboto", 12), borderwidth=2, relief="flat")
        self.h_len.grid(column=12, row=0, columnspan=1)
        


    def add_row(self, packet):
        self.packetcount += 1
        #buttons.configure(text=str(self.packetcount)+" "+str(packet.sourceIP)+" "+
        #        str(packet.destIP)+" "+str(packet.protocol)+" "+str("test"))
        #buttons.grid(row=(self.packetcount+10), column=0, columnspan=12, sticky="news")
        self.headers = ["Number", "Source", "Destination", "Protocol", "Information"]
        buttons = [Button() for i in range(0, len(self.headers))]

        
        for i in range(0, len(self.headers)):
            buttons[i] = Button(self.packetrows)
            
            if(self.headers[i]=="Number"):
                buttons[i].configure(text=str(self.packetcount), font=("roboto", 10), relief="flat")
                buttons[i].grid(row=(self.packetcount+10), column=0, sticky="news")
            elif(self.headers[i]=="Source"):
                buttons[i].configure(text=str(packet.sourceIP), font=("roboto", 10), relief="flat")
                buttons[i].grid(row=(self.packetcount+10), column=1, sticky="news")
            elif(self.headers[i]=="Destination"):
                buttons[i].configure(text=str(packet.destIP), font=("roboto", 10), relief="flat")
                buttons[i].grid(row=(self.packetcount+10), column=6, sticky="news")
            elif(self.headers[i]=="Protocol"):
                buttons[i].configure(text=str(packet.protocol), font=("roboto", 10), relief="flat")
                buttons[i].grid(row=(self.packetcount+10), column=11, sticky="news")
            elif(self.headers[i]=="Information"):
                buttons[i].configure(text=str("test"), font=("roboto", 10), relief="flat")
                buttons[i].grid(row=(self.packetcount+10), column=12, sticky="news")
        
        self.packetrows.update_idletasks()


class DataFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.dataframe = Frame(self, bg="grey", width=800, height=300)
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

    def register_packet(self, packet):
        self.statusbar.change_status("Status: Capturing Packets...")
        self.packetframe.add_row(packet)
        
    def add_toolbar_command(self, name, func):
        self.toolbar.add_command(name, func)

    def render(self):
        self.mainloop()
    
