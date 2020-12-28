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
        
        self.headers = ["Number", "Source", "Destination", "Protocol", "Header Length"]
        self.packetcount = 0
        self.all_rows = []
        self.highlighted_row = 0
        self.buttonsinrow = []
        self.buttoncount = 0

        
        # make the outer packet frame, then make the inner packet frame to hold the headers
        self.packetframe = Frame(self, bg="grey")
        self.packetframe.pack(side="left", fill="both", padx=2, pady=2)
        self.packetframe2 = Frame(self.packetframe, bg="lightgrey", pady=2, padx=2, height=668, width=510, bd=0)
        self.packetframe2.grid(row=0, column=0, sticky="news", pady=2, padx=2)
        self.packetframe.pack_propagate(0)
        self.packetframe2.grid_propagate(0)

        # make the canvas & scrollbar for where we are holding our packets
        self.packetrows = Canvas(self.packetframe2, bg="lightgrey",relief="flat", height=655, width=480, bd=0)
        self.packetrows_vsb = Scrollbar(self.packetframe2, orient="vertical", command=self.packetrows.yview, bd=0, bg="white", activebackground="white", highlightcolor="white")
       
        self.packetframe3 = Frame(self.packetframe2, bg="lightgrey", height=655, width=480, bd=0)
        self.packetrows.create_window((0,0), anchor="nw", window=self.packetframe3) 
        self.packetrows.update_idletasks()

        self.packetrows.configure(scrollregion=self.packetrows.bbox("all"), yscrollcommand=self.packetrows_vsb.set)

        #self.packetrows.grid_propagate(0)
        self.packetrows.grid(row=0, column=0, sticky="news", pady=2, padx=2)
        self.packetrows_vsb.grid(row=0, column=18, sticky="ns")


        # make the headers
        self.h_number = Label(self.packetframe3, bg="white", cursor="dot", 
            text="Number", font=("roboto", 12), borderwidth=2, relief="flat")
        self.h_number.grid(column=0, row=0, columnspan=1)
        self.h_src = Label(self.packetframe3, bg="white", cursor="dot",
            text="     Source     ", font=("roboto", 12), borderwidth=2, relief="flat")
        self.h_src.grid(column=1, row=0)
        self.h_dest = Label(self.packetframe3, bg="white", cursor="dot",
            text="     Destination     ", font=("roboto", 12), borderwidth=2, relief="flat")
        self.h_dest.grid(column=6, row=0)
        self.h_proto = Label(self.packetframe3, bg="white", cursor="dot",
            text="Protocol", font=("roboto", 12), borderwidth=2, relief="flat")
        self.h_proto.grid(column=11, row=0, columnspan=1)
        self.h_len = Label(self.packetframe3, bg="white", cursor="dot", 
            text="   Header Length   ", font=("roboto", 12), borderwidth=2, relief="flat")
        self.h_len.grid(column=12, row=0, columnspan=1)
        
    def add_row(self, packet, packetid):
        self.packetcount += 1
        self.capturing = True
        # create a new row of buttons
        self.buttons = [Button() for i in range(0, len(self.headers))]
        self.buttonsinrow = []

        # set the buttons, configure and pack them
        for i in range(0, len(self.headers)):
            self.buttoncount +=1
            self.buttons[i] = Button(self.packetframe3)
            if(self.headers[i]=="Number"):
                self.buttons[i].configure(text=str(self.packetcount))
                self.buttons[i].grid(row=(self.packetcount+10), column=0, sticky="news")
            elif(self.headers[i]=="Source"):
                self.buttons[i].configure(text=str(packet.sourceIP))
                self.buttons[i].grid(row=(self.packetcount+10), column=1, sticky="news")
            elif(self.headers[i]=="Destination"):
                self.buttons[i].configure(text=str(packet.destIP))
                self.buttons[i].grid(row=(self.packetcount+10), column=6, sticky="news")
            elif(self.headers[i]=="Protocol"):
                self.buttons[i].configure(text=str(packet.protocol))
                self.buttons[i].grid(row=(self.packetcount+10), column=11, sticky="news")
            elif(self.headers[i]=="Header Length"):
                self.buttons[i].configure(text=str(packet.headerLen), font=("roboto", 10), relief="flat")
                self.buttons[i].grid(row=(self.packetcount+10), column=12, sticky="news")
            self.buttons[i].configure(activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=0, command= lambda: self.on_click(packet, packetid))
            self.on_hover(self.buttons[i])
            self.buttonsinrow.append(self.buttons[i])
        self.all_rows.append(self.buttonsinrow)
        self.packetrows.update()
        self.packetrows.configure(scrollregion=self.packetrows.bbox("all"))
        
    
    def on_hover(self, button):
        button.bind("<Leave>", func=lambda e: button.config(background="white"))
        button.bind("<Enter>", func=lambda e: button.config(background="lightblue"))
    
    def on_click(self, packet, packetid):
        specific_row = self.all_rows[packetid-1]
        old_row = self.all_rows[self.highlighted_row]

        # set current row highlighted
        for i in range(0, len(self.headers)):
            specific_row[i].configure(state=ACTIVE)

        # set old row not highlighted
        for i in range(0, len(self.headers)):
            old_row[i].configure(state=NORMAL)

        self.highlighted_row = packetid - 1

        # actually load data
        self.parent.dataframe.set_data(packet, packetid)

class DataFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.all_rows_hex = []
        self.all_rows_unicode = []

        # make a frame and a nested frame
        self.dataframe = Frame(self, bg="grey", width=800, height=300)
        self.dataframe.pack(side="bottom", fill="both", padx=2, pady=2)
        self.dataframe.pack_propagate(0)
        self.dataframe2 = Frame(self.dataframe, bg="lightgrey", width=400, height=150, pady=2, padx=2)
        self.dataframe2.pack(side="bottom", fill="both", padx=2, pady=2, expand=False)
        

        # make our canvases to hold unicode and hex text boxes
        self.hex_rows = Canvas(self.dataframe2, bg="white", relief="flat")
        self.hex_rows.grid(row=0, column=0, sticky="news", pady=2, padx=2, columnspan=1)
        self.unicode_rows = Canvas(self.dataframe2, bg="white", relief="flat")
        self.unicode_rows.grid(row=0, column=2, sticky="news", pady=2, padx=2)

        # make our header labels for description
        self.h_hex = Label(self.hex_rows, bg="white", cursor="dot", text="Hex", font=("roboto", 12), 
            borderwidth=2, relief="flat")
        self.h_hex.grid(column=0, row=0, columnspan=1)
        self.h_unic = Label(self.unicode_rows, bg="white", cursor="dot", text="Unicode", font=("roboto", 12), 
            borderwidth=2, relief="flat")
        self.h_unic.grid(column=0, row=0, columnspan=1)

        # make our text boxes to hold the actual data
        self.hex_text = Text(self.hex_rows, bg="white", relief="flat", padx=2, width=80, height=16)
        self.unicode_text = Text(self.unicode_rows, bg="white", relief="flat", pady=2, padx=2, width=78, height=16)
        self.hex_text.grid(row=1, column=0, sticky="news", pady=2, padx=2, columnspan=1)
        self.unicode_text.grid(row=1, column=0, sticky="news", pady=2, padx=2, columnspan=1)
        self.hex_text.grid_propagate(0)
        self.unicode_text.grid_propagate(0)

        # make our scrollbar for textboxes
        self.hex_vsb = Scrollbar(self.dataframe2, orient="vertical", command=self.hex_text.yview, bd=0, bg="white", activebackground="white", highlightcolor="white")
        self.unic_vsb = Scrollbar(self.dataframe2, orient="vertical", command=self.unicode_text.yview, bd=0, bg="white", activebackground="white", highlightcolor="white")
        self.hex_vsb.grid(row=0, column=1, sticky="news", pady=2, padx=2)
        self.unic_vsb.grid(row=0, column=3, sticky="news", pady=2, padx=2)
        self.hex_text.configure(yscrollcommand=self.hex_vsb.set)
        self.unicode_text.configure(yscrollcommand=self.unic_vsb.set)

    def set_data(self, packet, packetid):
        # set text box editable and pack our data
        self.hex_text.config(state=NORMAL)
        self.unicode_text.config(state=NORMAL)
        self.hex_text.delete(1.0, "end")
        self.hex_text.insert(1.0, packet.payload.data)
        self.unicode_text.delete(1.0, "end")
        self.unicode_text.insert(1.0, packet.payload.decdata)

        # set text box uneditable for the user
        self.hex_text.config(state=DISABLED)
        self.unicode_text.config(state=DISABLED)
        
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
        
class HeadersFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

class UserInterface(tk.Tk):
    def __init__(self):
        super().__init__(screenName="Packet Sniffer")
        self.geometry("1080x720")
        self.state('zoomed')
        self.title('Packet Sniffer')
        self.toolbar = ToolBar(self)
        self.statusbar = StatusBar(self)
        self.packetid = 0
        
        self.dataframe = DataFrame(self)
        self.packetframe = PacketFrame(self)

        self.dataframe.pack(side="bottom", fill="both", padx=2, pady=2, expand=True)
        self.packetframe.pack(side="left", fill="both", padx=2, pady=2, expand=True)

    def register_packet(self, packet):
        self.packetid += 1
        self.packetframe.add_row(packet, self.packetid)
        
    def add_toolbar_command(self, name, func):
        self.toolbar.add_command(name, func)

    def render(self):
        self.mainloop()
    
