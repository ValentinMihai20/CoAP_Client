from tkinter import *


class Base_Window:

    def __init__(self):
        self.window = Tk()
        self.window.wm_title('Browser CoAP')
        self.window.geometry("600x400")
        self.button_connect = Button(self.window, height=3, width=10, text="Connect", font="arial 15 bold",
                                     bg="#98fb98")
        self.button_disconnect = Button(self.window, height=3, width=10, text="Disconnect", font="arial 15 bold",
                                        bg="#ff0000")
        self.button_clearScreen = Button(self.window, height=3, width=10, text="Clear Screen", font="arial 15 bold",
                                         bg="#98fb98")
        self.button_exit = Button(self.window, height=3, width=10, text="Exit", font="arial 15 bold",
                                  bg="#98fb98")

        self.text_box = Text(self.window, height=25, width=66, font="arial 10", bg="white")
        self.text_box2 = Text(self.window, height=5, width=66, font="arial 10", bg="white")

        self.button_connect.place(x=450, y=50)
        self.button_clearScreen.place(x=450, y=150)
        self.button_exit.place(x=450, y=250)


app = Base_Window()
app.window.mainloop()
