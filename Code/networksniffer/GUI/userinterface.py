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
        self.packetrows_vsb = Scrollbar(self.packetframe2, orient="vertical", command=self.packetrows.yview, bd=0)
       
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
            text="   Packet Version  ", font=("roboto", 12), borderwidth=2, relief="flat")
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
                self.buttons[i].configure(text=("IPV"+str(packet.vers)), font=("roboto", 10), relief="flat")
                self.buttons[i].grid(row=(self.packetcount+10), column=12, sticky="news")
            self.buttons[i].configure(activebackground="lightgreen", highlightcolor="lightblue", background="white",
                borderwidth=0, command= lambda: self.on_click(packet, packetid))
            self.on_hover(self.buttons[i])
            self.buttonsinrow.append(self.buttons[i])
        self.all_rows.append(self.buttonsinrow)
        self.packetrows.update()
        self.packetrows.configure(scrollregion=self.packetrows.bbox("all"))
        
    
    def on_hover(self, button):
        if(button['bg']=="lightgreen"):
            button['activebackground'] = "lightgreen"
            button.bind("<Leave>", func=lambda e: button.config(background="lightgreen"))
            button.bind("<Enter>", func=lambda e: button.config(background="lightblue"))
        elif(button['bg']=="white"):
            button['activebackground'] = "white"
            button.bind("<Leave>", func=lambda e: button.config(background="white"))
            button.bind("<Enter>", func=lambda e: button.config(background="lightblue"))

    def on_click(self, packet, packetid):
        specific_row = self.all_rows[packetid-1]
        old_row = self.all_rows[self.highlighted_row]

        # set current row highlighted
        for i in range(0, len(self.headers)):
            specific_row[i].configure(bg="lightgreen")
            self.on_hover(specific_row[i])


        # set old row not highlighted
        for i in range(0, len(self.headers)):
            old_row[i].configure(bg="white")
            self.on_hover(old_row[i])

        self.highlighted_row = packetid - 1

        # load data into dataframe & tcpip stack graphic
        self.parent.dataframe.set_data(packet, packetid)
        self.parent.headerframe.set_data(packet, packetid)

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
        

        # make our canvases to hold unicode and hex text boxes and extra info
        self.hex_rows = Canvas(self.dataframe2, bg="white", relief="flat")
        self.hex_rows.grid(row=0, column=0, sticky="news", pady=2, padx=2, columnspan=1)
        self.unicode_rows = Canvas(self.dataframe2, bg="white", relief="flat")
        self.unicode_rows.grid(row=0, column=2, sticky="news", pady=2, padx=2)
        self.all_info_canvas = Canvas(self.dataframe2, bg="white", relief="flat")
        self.all_info_canvas.grid(row=0, column=4, sticky="news", pady=2, padx=2)

        # make our header labels for description
        self.h_hex = Label(self.hex_rows, bg="white", cursor="dot", text="Payload Hex", font=("roboto", 12), 
            borderwidth=2, relief="flat")
        self.h_hex.grid(column=0, row=0, columnspan=1)
        self.h_unic = Label(self.unicode_rows, bg="white", cursor="dot", text="Payload Unicode", font=("roboto", 12), 
            borderwidth=2, relief="flat")
        self.h_unic.grid(column=0, row=0, columnspan=1)
        self.h_allinfo = Label(self.all_info_canvas, bg="white", cursor="dot", text="All Information", font=("roboto", 12), 
            borderwidth=2, relief="flat")
        self.h_allinfo.grid(column=0, row=0, columnspan=1)

        # make our text boxes to hold the actual data
        self.hex_text = Text(self.hex_rows, bg="white", relief="flat", padx=2, width=80, height=16, selectbackground="lightgreen")
        self.unicode_text = Text(self.unicode_rows, bg="white", relief="flat", pady=2, padx=2, width=78, height=16, selectbackground="lightgreen")
        self.hex_text.grid(row=1, column=0, sticky="news", pady=2, padx=2, columnspan=1)
        self.unicode_text.grid(row=1, column=0, sticky="news", pady=2, padx=2, columnspan=1)
        self.hex_text.grid_propagate(0)
        self.unicode_text.grid_propagate(0)

        self.all_info_text = Text(self.all_info_canvas, bg="white", relief="flat", padx=2, width=67, height=16, selectbackground="lightgreen")
        self.all_info_text.grid(row=1, column=0, sticky="news", pady=2, padx=2, columnspan=1)
        self.all_info_text.grid_propagate(0)


        # make our scrollbar for textboxes
        self.hex_vsb = Scrollbar(self.dataframe2, orient="vertical", command=self.hex_text.yview, bd=0, bg="white", activebackground="white", highlightcolor="white")
        self.unic_vsb = Scrollbar(self.dataframe2, orient="vertical", command=self.unicode_text.yview, bd=0, bg="white", activebackground="white", highlightcolor="white")
        self.hex_vsb.grid(row=0, column=1, sticky="news", pady=2, padx=2)
        self.unic_vsb.grid(row=0, column=3, sticky="news", pady=2, padx=2)
        self.hex_text.configure(yscrollcommand=self.hex_vsb.set)
        self.unicode_text.configure(yscrollcommand=self.unic_vsb.set)
        self.all_info_vsb = Scrollbar(self.dataframe2, orient="vertical", command=self.hex_text.yview, bd=0, bg="white", activebackground="white", highlightcolor="white")
        self.all_info_vsb.grid(row=0, column=5, sticky="news", pady=2, padx=2)
        self.all_info_text.configure(yscrollcommand=self.all_info_vsb.set)


    def set_data(self, packet, packetid):
        # set text box editable and pack our data
        self.hex_text.config(state=NORMAL)
        self.unicode_text.config(state=NORMAL)
        self.all_info_text.config(state=NORMAL)

        self.hex_text.delete(1.0, "end")
        self.hex_text.insert(1.0, packet.payload.data)
        self.unicode_text.delete(1.0, "end")
        self.unicode_text.insert(1.0, packet.payload.decdata)
        self.all_info_text.delete(1.0, "end")
        self.all_info_text.insert(1.0, ("Source IP: " + str(packet.sourceIP) + "\n"))
        self.all_info_text.insert(2.0, ("Destination IP: " + str(packet.destIP) + "\n"))
        self.all_info_text.insert(3.0, ("Version: " + str(packet.vers) + "\n"))
        self.all_info_text.insert(4.0, ("Length: " + str(packet.len) + "\n"))
        self.all_info_text.insert(5.0, ("Header Length: " + str(packet.headerLen) + "\n"))
        self.all_info_text.insert(6.0, ("Protocol: " + str(packet.protocol) + "\n"))
        self.all_info_text.insert(7.0, ("Source Port: " + str(packet.srcPort) + "\n"))
        self.all_info_text.insert(8.0, ("Destination Port: " + str(packet.destPort) + "\n"))
        self.all_info_text.insert(9.0, ("Sequence Number: " + str(packet.seqNum) + "\n"))
        if(packet.protocol=="TCP"):
            self.all_info_text.insert(10.0, ("Flags: ", packet.flags))
        else:
            pass

        # set text box uneditable for the user
        self.hex_text.config(state=DISABLED)
        self.unicode_text.config(state=DISABLED)
        self.all_info_text.config(state=DISABLED)

        
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
        
class ControlFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        # make outer and inner frame
        self.cpframe_outer = Frame(self, bg="grey")
        self.cpframe_outer.pack(side="left", fill="both", padx=2, pady=2)
        self.cpframe_inner = Frame(self.cpframe_outer, bg="lightgrey", pady=2, padx=2, height=668, width=515, bd=0)
        self.cpframe_inner.grid(row=0, column=0, pady=2, padx=2)
        self.cpframe_outer.pack_propagate(0)
        self.cpframe_inner.grid_propagate(0)

        # make the canvas to hold our 2 frames
        self.cp_widget_canvas = Canvas(self.cpframe_inner, bg="lightgrey", relief="flat", height=655, width=502, bd=0)
        self.cp_widget_canvas.grid(row=0, column=0, pady=2, padx=2, sticky="news")
        self.cp_widget_canvas.grid_propagate(0)
        self.cp_widget_canvas.update_idletasks()

        # make our 2 frames
        self.capture_frame = Frame(self.cp_widget_canvas, bg="lightgrey", relief="flat", height=327, width=502, bd=2)
        self.filter_frame = Frame(self.cp_widget_canvas, bg="lightgrey", relief="flat", height=327, width=502, bd=2)
        self.capture_frame.pack(side="top", fill="both", padx=2, pady=2)
        self.capture_frame.pack_propagate(0)
        self.capture_frame.update_idletasks()
        self.filter_frame.pack(side="bottom", fill="both", padx=2, pady=2)
        self.filter_frame.pack_propagate(0)
        self.filter_frame.update_idletasks()

        # pack our capture frame with relevant widgets & data
        self.capture_header = Label(self.capture_frame, bg="lightgrey", cursor="dot", 
            text="Capture", font=("roboto", 12), borderwidth=2, relief="flat", anchor="center")
        self.capture_header.pack(side="top", padx=2, pady=2)

        # pack our filter frame with relevant widgets & data
        self.filter_header = Label(self.filter_frame, bg="lightgrey", cursor="dot", 
            text="Filter", font=("roboto", 12), borderwidth=2, relief="flat", anchor="center")
        self.filter_header.pack(side="top", padx=2, pady=2)

        #// important note, our filter frame must contain 2 sub frames in order to house the different filters
        self.filter_subframe1 = Frame(self.filter_frame, bg="lightgrey", relief="flat", height=327, width=251, bd=2)
        self.filter_subframe2 = Frame(self.filter_frame, bg="lightgrey", relief="flat", height=327, width=251, bd=2)
        self.filter_subframe1.pack(side="left", fill="both", padx=2, pady=2)
        self.filter_subframe2.pack(side="right", fill="both", padx=2, pady=2)
        self.filter_subframe1.pack_propagate(0)
        self.filter_subframe2.pack_propagate(0)

        self.app_layer_header = Label(self.filter_subframe1, bg="lightgrey", cursor="dot", 
            text="Application Layer", font=("roboto", 12), borderwidth=2, relief="flat", anchor="center")
        self.net_layer_header = Label(self.filter_subframe2, bg="lightgrey", cursor="dot", 
            text="Transport Layer", font=("roboto", 12), borderwidth=2, relief="flat", anchor="center")
        self.app_layer_header.pack(side="top", padx=2, pady=2)
        self.net_layer_header.pack(side="top", padx=2, pady=2)

        self.app_desc = Label(self.filter_subframe1, bg="lightgrey", cursor="dot", 
            text="Filter on specific ports, e.g 80 (HTTP)", font=("roboto", 10), borderwidth=2, relief="flat", anchor="center")
        self.net_desc = Label(self.filter_subframe2, bg="lightgrey", cursor="dot", 
            text="Filter on common protocols, e.g TCP", font=("roboto", 10), borderwidth=2, relief="flat", anchor="center")
        self.app_desc.pack(side="top", padx=2, pady=2)
        self.net_desc.pack(side="top", padx=2, pady=2)

        self.tcp_butt = Button(self.filter_subframe2, text="TCP", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, command= lambda: self.on_click(self.tcp_butt), width=8, height=3, font=("roboto", 18))
        self.tcp_butt.pack(side="top", padx=2, pady=2)
        self.udp_butt = Button(self.filter_subframe2, text="UDP", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, command= lambda: self.on_click(self.udp_butt), width=8, height=3, font=("roboto", 18))
        self.udp_butt.pack(side="top", padx=2, pady=2)
        self.on_hover(self.tcp_butt)
        self.on_hover(self.udp_butt)

        # make grid of suggested protocols
        self.grid_suggested_protocols = Frame(self.filter_subframe1, bg="lightgrey", relief="flat", height=100, width=251, bd=2)
        self.grid_suggested_protocols.pack(side="bottom", padx=2, pady=2)
        
        self.http_butt = Button(self.grid_suggested_protocols, text="HTTP", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, command= lambda: self.on_click(self.http_butt), font=("roboto", 12), padx=2, pady=2)
        self.http_butt.grid(row=0, column=0, padx=2, pady=2)
        self.on_hover(self.http_butt)
        self.ftp_butt = Button(self.grid_suggested_protocols, text="FTP", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, command= lambda: self.on_click(self.ftp_butt), font=("roboto", 12), padx=2, pady=2)
        self.ftp_butt.grid(row=0, column=1, padx=2, pady=2)
        self.on_hover(self.ftp_butt)
        self.ssh_butt = Button(self.grid_suggested_protocols, text="SSH", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, command= lambda: self.on_click(self.ssh_butt), font=("roboto", 12), padx=2, pady=2)
        self.ssh_butt.grid(row=0, column=2, padx=2, pady=2)
        self.on_hover(self.ssh_butt)
        self.rdp_butt = Button(self.grid_suggested_protocols, text="RDP", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, command= lambda: self.on_click(self.rdp_butt), font=("roboto", 12), padx=2, pady=2)
        self.rdp_butt.grid(row=2, column=1, padx=2, pady=2)
        self.on_hover(self.rdp_butt)
        self.dns_butt = Button(self.grid_suggested_protocols, text="DNS", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, command= lambda: self.on_click(self.dns_butt), font=("roboto", 12), padx=2, pady=2)
        self.dns_butt.grid(row=1, column=1, padx=2, pady=2)
        self.on_hover(self.dns_butt)
        self.pop_butt = Button(self.grid_suggested_protocols, text="POP", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, command= lambda: self.on_click(self.pop_butt), font=("roboto", 12), padx=2, pady=2)
        self.pop_butt.grid(row=1, column=2, padx=2, pady=2)
        self.on_hover(self.pop_butt)
        self.smtp_butt = Button(self.grid_suggested_protocols, text="SMTP", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, command= lambda: self.on_click(self.smtp_butt), font=("roboto", 12), padx=2, pady=2)
        self.smtp_butt.grid(row=1, column=0, padx=2, pady=2)
        self.on_hover(self.smtp_butt)
        self.imap_butt = Button(self.grid_suggested_protocols, text="IMAP", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, command= lambda: self.on_click(self.imap_butt), font=("roboto", 12), padx=2, pady=2)
        self.imap_butt.grid(row=2, column=0, padx=2, pady=2)
        self.on_hover(self.imap_butt)
        self.slp_butt = Button(self.grid_suggested_protocols, text="SLP", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, command= lambda: self.on_click(self.slp_butt), font=("roboto", 12), padx=2, pady=2)
        self.slp_butt.grid(row=2, column=2, padx=2, pady=2)
        self.on_hover(self.slp_butt)
        
        self.port_entry_header = Label(self.filter_subframe1, bg="lightgrey", cursor="dot", 
            text=" Specific Port:", font=("roboto", 10), borderwidth=2, relief="flat", anchor="e")
        self.port_entry_header.pack(side="left", padx=2, pady=2)
        self.port_entry = Entry(self.filter_subframe1, text="Specific Port", font=("roboto", 10))
        self.port_entry.pack(side="right", padx=2, pady=2)

        self.capture_subframe1 = Frame(self.capture_frame, bg="lightgrey", relief="flat", height=93, width=502, bd=2)
        self.capture_subframe2 = Frame(self.capture_frame, bg="lightgrey", relief="flat", height=93, width=502, bd=2)
        self.capture_subframe3 = Frame(self.capture_frame, bg="lightgrey", relief="flat", height=93, width=502, bd=2)
        self.capture_subframe1.pack(side="top", fill="both", padx=2, pady=2)
        self.capture_subframe2.pack(side="top", fill="both", padx=2, pady=2)
        self.capture_subframe3.pack(side="top", fill="both", padx=2, pady=2)
        self.capture_subframe1.pack_propagate(0)
        self.capture_subframe2.pack_propagate(0)
        self.capture_subframe3.pack_propagate(0)

        # add spacing
        self.capture_subframe1.grid_columnconfigure(1, minsize=25)
        self.capture_subframe1.grid_columnconfigure(4, minsize=78)
        self.capture_subframe1.grid_columnconfigure(6, minsize=78)
        #command= lambda: self.on_click(self.stop_cap_button)
        # make capture widgets
        self.start_cap_label = Label(self.capture_subframe1, text="Start Capture", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, 
                font=("roboto", 12), padx=2, pady=2, anchor="center", bg="lightgrey")
        self.start_cap_label.grid(row=0, column=2, padx=2, pady=2, sticky="news")
        self.stop_cap_label = Label(self.capture_subframe1, text="Stop Capture", activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, 
                font=("roboto", 12), padx=2, pady=2, anchor="center", bg="lightgrey")
        self.stop_cap_label.grid(row=0, column=5, padx=2, pady=2, sticky="news")

        self.startimg = PhotoImage(file="C:/Users/Bailey/Desktop/Project/Code/networksniffer/GUI/img/start.png")
        self.stopimg = PhotoImage(file="C:/Users/Bailey/Desktop/Project/Code/networksniffer/GUI/img/stop.png")
        self.start_cap_button = Button(self.capture_subframe1, image=self.startimg, activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, 
                font=("roboto", 12), padx=2, pady=2, anchor="center")
        self.start_cap_button.grid(row=0, column=3, padx=2, pady=2, sticky="news")
        self.stop_cap_button = Button(self.capture_subframe1, image=self.stopimg, activebackground="lightblue", highlightcolor="lightblue", background="white",
                borderwidth=2, 
                font=("roboto", 12), padx=2, pady=2, anchor="center")
        self.stop_cap_button.grid(row=0, column=6, padx=2, pady=2, sticky="news")

    def set_button(self, name, func):
        if(name=="Start Capture"):
            self.start_cap_button.configure(command=func)
        elif(name=="Stop Capture"):
            self.stop_cap_button.configure(command=func)

    def on_hover(self, button):
        if(button['bg']=="lightgreen"):
            button['activebackground'] = "lightgreen"
            button.bind("<Leave>", func=lambda e: button.config(background="lightgreen"))
            button.bind("<Enter>", func=lambda e: button.config(background="lightblue"))
        elif(button['bg']=="white"):
            button['activebackground'] = "white"
            button.bind("<Leave>", func=lambda e: button.config(background="white"))
            button.bind("<Enter>", func=lambda e: button.config(background="lightblue"))

    def on_click(self, button):
        self.on_hover(button)
        if(button['activebackground']=="white"):
            button.configure(bg="lightgreen")
        elif(button['activebackground']=="lightgreen"):
            button.configure(bg="white")
        self.on_hover(button)
        
        # actually load data
        
class HeaderFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        # make outer and inner frame
        self.headersframe_outer = Frame(self, bg="grey")
        self.headersframe_outer.pack(side="left", fill="both", padx=2, pady=2)
        self.headersframe_inner = Frame(self.headersframe_outer, bg="lightgrey", pady=2, padx=2, height=668, width=856, bd=0)
        self.headersframe_inner.grid(row=0, column=0, pady=2, padx=2)
        self.headersframe_outer.pack_propagate(0)
        self.headersframe_inner.grid_propagate(0)

        # make the canvas to hold our widgets
        self.headers_widget_canvas = Canvas(self.headersframe_inner, bg="lightgrey",relief="flat", height=655, width=843, bd=0)
        self.headers_widget_canvas.grid(row=0, column=0, pady=2, padx=2, sticky="ew")
        self.headers_widget_canvas.grid_propagate(0)
        self.headers_widget_canvas.update_idletasks()

        # make 3 frames to hold network / transport / application headers
        #self.network_frame0 = Frame(self.headers_widget_canvas, bg="white", pady=2, padx=2, height=222, width=856, bd=0)
        #self.transport_frame0 = Frame(self.headers_widget_canvas, bg="white", pady=2, padx=2, height=222, width=856, bd=0)
        #self.application_frame0 = Frame(self.headers_widget_canvas, bg="white", pady=2, padx=2, height=222, width=856, bd=0)
        self.network_frame1 = Frame(self.headers_widget_canvas, bg="white", pady=2, padx=2, height=222, width=856, bd=0)
        self.transport_frame1 = Frame(self.headers_widget_canvas, bg="white", pady=2, padx=2, height=222, width=856, bd=0)
        self.application_frame1 = Frame(self.headers_widget_canvas, bg="white", pady=2, padx=2, height=222, width=856, bd=0)
        self.network_frame1.grid(row=2, column=0, sticky="e")
        self.transport_frame1.grid(row=1, column=0, sticky="e")
        self.application_frame1.grid(row=0, column=0, sticky="e")

        # make label about what this is
        self.overall_label = Label(self.headers_widget_canvas, bg="lightgrey", cursor="dot", 
            text="Packet Decomposition", font=("roboto", 12), borderwidth=2, relief="flat", anchor="nw", height=10, width=50, padx=2, pady=2)
        self.overall_label.grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.overall_label.grid_propagate(0)

        self.network_frame2 = Frame(self.network_frame1, bg="lightpink", pady=2, padx=2, height=215, width=841, bd=0)
        self.transport_frame2 = Frame(self.transport_frame1, bg="lightgreen", pady=2, padx=2, height=215, width=503, bd=0)
        self.application_frame2 = Frame(self.application_frame1, bg="lightblue", pady=2, padx=2, height=215, width=233, bd=0)
        self.network_frame2.grid(row=0, column=0, sticky="e")
        self.transport_frame2.grid(row=0, column=0, sticky="e")
        self.application_frame2.grid(row=0, column=0, sticky="e")
        self.network_frame3 = Frame(self.network_frame2, bg="violet red", pady=2, padx=2, height=211, width=500, bd=0)
        self.transport_frame3 = Frame(self.transport_frame2, bg="green", pady=2, padx=2, height=211, width=230, bd=0)
        self.application_frame3 = Frame(self.application_frame2, bg="blue", pady=2, padx=2, height=211, width=230, bd=0)
        self.network_frame3.pack(side="right", pady=2, padx=2)
        self.transport_frame3.pack(side="right", pady=2, padx=2)
        self.application_frame3.pack(side="right", pady=2, padx=2)
        self.network_frame3.pack_propagate(0)
        self.application_frame3.pack_propagate(0)
        self.transport_frame3.pack_propagate(0)
        self.network_frame2.pack_propagate(0)
        self.application_frame2.pack_propagate(0)
        self.transport_frame2.pack_propagate(0)
        self.network_frame4 = Frame(self.network_frame2, bg="violet red", pady=2, padx=2, height=210, width=250, bd=0)
        self.transport_frame4 = Frame(self.transport_frame2, bg="green", pady=2, padx=2, height=210, width=20, bd=0)
        self.network_frame4.pack(side="left", pady=2, padx=2)
        self.transport_frame4.pack(side="left", pady=2, padx=2)

        self.payload_label_app = Label(self.application_frame3, bg="lightblue", cursor="dot", 
            text="Payload: ", font=("roboto", 12), borderwidth=2, relief="flat", anchor="center", height=150, width=200)
        self.payload_label_tra = Label(self.transport_frame3, bg="lightgreen", cursor="dot", 
            text="Payload: ", font=("roboto", 12), borderwidth=2, relief="flat", anchor="center", height=150, width=200)
        self.payload_label_net = Label(self.network_frame3, bg="lightpink", cursor="dot", 
            text="Payload: ", font=("roboto", 12), borderwidth=2, relief="flat", anchor="center", height=150, width=450)
        self.payload_label_app.pack(padx=2, pady=2, fill="both")
        self.payload_label_tra.pack(padx=2, pady=2, fill="both")
        self.payload_label_net.pack(padx=2, pady=2, fill="both")
        self.header_label_tra = Label(self.transport_frame4, bg="lightgreen", cursor="dot", 
            text="Header Data: ", font=("roboto", 12), borderwidth=2, relief="flat", anchor="center", height=150, width=200, wraplength=240)
        self.header_label_net = Label(self.network_frame4, bg="lightpink", cursor="dot", 
            text="Header Data: ", font=("roboto", 12), borderwidth=2, relief="flat", anchor="center", height=150, width=400, wraplength=300)
        self.header_label_tra.pack(padx=2, pady=2, fill="both")
        self.header_label_net.pack(padx=2, pady=2, fill="both")

    def set_data(self, packet, packetid):
        self.payload_label_app.configure(text=("Payload: " + str(packet.len) + " bytes long"))
        self.payload_label_net.configure(text=("Payload: " + str(packet.len + packet.dOffset) + " bytes long"))
        self.payload_label_tra.configure(text=("Payload: " + str(packet.len) + " bytes long"))

        self.overall_label.configure(text=("Packet Decomposition of " + 
            str(packet.protocol) + " packet " + str(packetid)))

        self.header_label_net.configure(text=("Header Data: \n" + 
            "Source IP: " + str(packet.sourceIP) + "\n" +
            "Destination IP: " + str(packet.destIP) + "\n" +
            "Version: " + str(packet.vers) + "\n" +
            "Header Length: " + str(packet.headerLen) + "\n" +
            "Protocol: " + str(packet.protocol) + "\n" +
            "Time to Live: " + str(packet.ttl) + "\n"))
        self.header_label_tra.configure(text=("Header Data: \n" + 
            "Source Port: " + str(packet.srcPort) + "\n" +
            "Destination Port: " + str(packet.destPort) + "\n" +
            "Sequence Number: " + str(packet.seqNum) + "\n" +
            "Header Length: " + str(packet.dOffset) + "\n"))
        if(packet.protocol=="TCP"):
            self.header_label_tra.configure(text=("Header Data: \n" + 
            "Source Port: " + str(packet.srcPort) + "\n" +
            "Destination Port: " + str(packet.destPort) + "\n" +
            "Sequence Number: " + str(packet.seqNum) + "\n" +
            "Header Length: " + str(packet.dOffset) + "\n" +
            "Flags: " + str(packet.flags) + "\n"))
        

class UserInterface(tk.Tk):
    def __init__(self):
        super().__init__(screenName="Packet Sniffer")
        self.geometry("1080x720")
        self.iconphoto(False, 
            tk.PhotoImage(file='C:/Users/Bailey/Desktop/Project/Code/networksniffer/GUI/img/package.png'))
        self.state('zoomed')
        self.title('Packet Sniffer')
        self.toolbar = ToolBar(self)
        self.statusbar = StatusBar(self)
        self.packetid = 0
        
        self.dataframe = DataFrame(self)
        self.dataframe.pack(side="bottom", fill="both", padx=2, pady=2, expand=True)

        self.packetframe = PacketFrame(self)
        self.packetframe.pack(side="left", fill="both", padx=2, pady=2, expand=True)

        self.controlframe = ControlFrame(self)
        self.controlframe.pack(side="left", fill="both", padx=2, pady=2, expand=True)

        self.headerframe = HeaderFrame(self)
        self.headerframe.pack(side="left", fill="both", padx=2, pady=2, expand=True)

    def register_packet(self, packet):
        self.packetid += 1
        self.packetframe.add_row(packet, self.packetid)
        
    def add_toolbar_command(self, name, func):
        self.toolbar.add_command(name, func)

    def add_button_command(self, name, func):
        self.controlframe.set_button(name, func)

    def render(self):
        self.mainloop()
    
