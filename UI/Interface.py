from tkinter import *


# fn = StringVar()


class Base_Window:

    def __init__(self):
        self.window = Tk()
        self.window.wm_title('Browser CoAP')
        self.window.geometry("400x400")
        self.button_connect = Button(self.window, text="Connect", width=20, bg='white', fg='black')
        self.button_connect.place(x=100, y=100)
        self.connect_text = Label(self.window, text="Conectare la server", width=30, font=("arial", 10, "bold"))
        self.connect_text.place(x=50, y=50)


# class Connect_Window:

#    def __init__(self):
#        self.window = Tk()
#        self.window.wm_title('Connecting')
#        self.window.geometry("200x200")
#        self.server_ip_entry = Entry(self.window, textvar=fn)
#        self.server_ip_entry.place(x=100, y=50)
#        self.server_ip_text = Label(self.window, text="Server IP:", width=20, font=("arial", 10, "bold"))
#        self.server_ip_text.place(x=50, y=50)


app = Base_Window()
app.window.mainloop()
