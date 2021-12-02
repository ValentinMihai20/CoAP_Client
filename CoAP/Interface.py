from tkinter import *


# fn = StringVar()


class Base_Window:

    def __init__(self):
        self.window = Tk()
        self.window.wm_title('Browser CoAP')
        self.window.geometry("600x400")
        self.button_connect = Button(self.window, height=3, width=10, text="Connect", font="arial 15 bold", bg="#98fb98")
        self.button_disconnect = Button(self.window, height=3, width=10, text="Disconnect", font="arial 15 bold", bg="#ff0000")
        self.button_clearScreen = Button(self.window, height=3, width=10, text="Clear Screen", font="arial 15 bold", bg="#98fb98")
        self.button_exit = Button(self.window, height=3, width=10, text="Exit", font="arial 15 bold", bg="#98fb98")

        self.button_connect.place(x=450, y=50)
        self.button_clearScreen.place(x=450, y=150)
        self.button_exit.place(x=450, y=250)

# class Connect_Window:

#    def __init__(self):
#        self.window = Tk()
#        self.window.wm_title('***Connecting to the server***')
#        self.window.geometry("200x200")
#        self.server_ip_entry = Entry(self.window, textvar=fn)
#        self.server_ip_entry.place(x=100, y=50)
#        self.server_ip_text = Label(self.window, text="Server IP:", width=20, font=("arial", 10, "bold"))
#        self.server_ip_text.place(x=50, y=50)

app = Base_Window()
app.window.mainloop()
