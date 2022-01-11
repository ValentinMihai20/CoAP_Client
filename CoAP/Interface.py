from tkinter import *
import CoAP.Client as client
import threading


class Base_Window:
    thread = threading.Thread(target=client.Client.client_connect)

    def __init__(self):
        self.window = Tk()
        self.window.wm_title('Browser CoAP')
        self.window.geometry("650x500")
        self.button_connect = Button(self.window, height=3, width=9, text="Connect", font="arial 15 bold",
                                     bg="#98fb98", command=self.start_client)
        self.button_disconnect = Button(self.window, height=3, width=9, text="Disconnect", font="arial 15 bold",
                                        bg="#ff0000", command=self.close_client)
        self.button_confirmable = Button(self.window, height=3, width=9, text="Confirmable", font="arial 15 bold",
                                         bg="#98fb98")
        self.button_clearScreen = Button(self.window, height=3, width=9, text="Clear Screen", font="arial 15 bold",
                                         bg="#98fb98", command=self.clear_screen)
        self.button_exit = Button(self.window, height=3, width=9, text="Exit", font="arial 15 bold", bg="#98fb98",
                                  command=self.exit)
        self.button_send = Button(self.window, height=2, width=9, text="-> Send", font="arial 15 bold", bg="#00ffff",
                                  command=self.send_message)

        self.text_box = Text(self.window, height=24, width=75, font="arial 10", bg="#eeeeee")
        self.text_box.config(state=DISABLED)
        self.text_box2 = Text(self.window, height=5, width=75, font="arial 10", bg="#eeeeee")

        self.button_connect.place(x=531, y=0)
        self.button_confirmable.place(x=531, y=100)
        self.button_clearScreen.place(x=531, y=200)
        self.button_exit.place(x=531, y=300)
        self.button_send.place(x=531, y=410)
        self.text_box.place(x=0, y=0)
        self.text_box2.place(x=0, y=400)


    def print_message(self, message):
        self.text_box.config(state=NORMAL)
        self.text_box.insert(END, ">> " + message + "\n")  # 1.0 insereaza la inceput / END insereaza la sfarsit
        self.text_box.config(state=DISABLED)

    def start_client(self):
        client.Client.__init__()
        self.__class__.thread = threading.Thread(target=client.Client.client_connect)
        self.__class__.thread.start()

        print('Connecting to the server...')
        self.button_connect.place_forget()
        self.button_disconnect.place(x=531, y=0)
        # self.text_box.place(x=0, y=0)

        self.print_message("Connected to the server!")

    def close_client(self):
        client.Client.client_disconnect()

        print('Disconnecting from the server...')
        self.button_disconnect.place_forget()
        self.button_connect.place(x=531, y=0)
        self.print_message("Disconnected from the server!")

    def exit(self):
        self.window.destroy()

    # clears the screen with a button

    def clear_screen(self):
        print('--Clearing Screen')
        self.text_box.config(state=NORMAL)
        self.text_box.delete(1.0, "end")

    def send_message(self):
        self.text_box2.config(state=NORMAL)
        self.text_box2.delete(1.0, "end")


app = Base_Window()
app.window.mainloop()