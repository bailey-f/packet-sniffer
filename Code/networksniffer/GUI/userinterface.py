import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.toolbar = tk.Frame(self, bg="blue")
        self.test = tk.Button(self.toolbar, text="test", command="doNothing")
        self.test.pack(side="left", padx=2, pady=2)
        self.toolbar.pack(side="top", fill="x")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
        
    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()