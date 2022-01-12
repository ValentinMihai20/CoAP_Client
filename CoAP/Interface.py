from tkinter import *
import threading

import CoAP.Client as client
import CoAP.Message


class BaseWindow:
    thread = threading.Thread(target=client.Client.client_connect)
    received_message = None
    response_message = None
    window = None
    button_connect = None
    button_disconnect = None
    button_confirmable = None
    button_non_confirmable = None
    button_acknowledgement = None
    button_reset = None
    button_clearScreen = None
    button_exit = None
    button_send = None
    text_box =  None
    text_box2 = None

    @classmethod
    def __init__(cls):
        cls.received_message = CoAP.Message.Message('Server')
        cls.response_message = CoAP.Message.Message('Client')
        cls.window = Tk()

        cls.button_connect = Button(cls.window, height=3, width=14, text="Connect", font="arial 15 bold",
                                    bg="#98fb98", command=cls.start_client)
        cls.button_disconnect = Button(cls.window, height=3, width=14, text="Disconnect", font="arial 15 bold",
                                       bg="#ff0000", command=cls.close_client)
        cls.button_confirmable = Button(cls.window, height=3, width=14, text="Confirmable",
                                        font="arial 15 bold", bg="#98fb98", command=cls.conf)
        cls.button_non_confirmable = Button(cls.window, height=3, width=14, text="Non-Confirmable",
                                            font="arial 15 bold", bg="#98fb98", command=cls.non_conf)
        cls.button_clearScreen = Button(cls.window, height=3, width=14, text="Clear Screen", font="arial 15 bold",
                                        bg="#98fb98", command=cls.clear_screen)
        cls.button_exit = Button(cls.window, height=3, width=14, text="Exit", font="arial 15 bold", bg="#98fb98",
                                 command=cls.exit)
        cls.button_send = Button(cls.window, height=2, width=14, text="-> Send", font="arial 15 bold", bg="#00ffff",
                                 command=cls.send_message)

        cls.text_box = Text(cls.window, height=24, width=75, font="arial 10", bg="#eeeeee")
        cls.text_box.config(state=DISABLED)
        cls.text_box2 = Text(cls.window, height=5, width=75, font="arial 10", bg="#eeeeee")

    @classmethod
    def start_application(cls):
        cls.window.wm_title('Browser CoAP')
        cls.window.geometry("750x500")

        cls.button_connect.place(x=531, y=0)
        cls.button_confirmable.place(x=531, y=100)
        cls.button_clearScreen.place(x=531, y=200)
        cls.button_exit.place(x=531, y=300)
        cls.button_send.place(x=531, y=410)
        cls.text_box.place(x=0, y=0)
        cls.text_box2.place(x=0, y=400)

        cls.window.mainloop()

    @classmethod
    def print_message(cls, message):
        cls.text_box.config(state=NORMAL)
        cls.text_box.insert(END, ">> " + message + "\n")
        cls.text_box.config(state=DISABLED)



    @classmethod
    def non_conf(cls):
        cls.button_non_confirmable.place_forget()
        cls.button_confirmable.place(x=531, y=100)
        cls.print_message("Using confirmable")
        cls.response_message.set_msg_type(0)
        # nu stim daca functioneaza

    @classmethod
    def conf(cls):
        cls.button_confirmable.place_forget()
        cls.button_non_confirmable.place(x=531, y=100)
        cls.print_message("Using non_confirmable")
        cls.response_message.set_msg_type(1)
        # nu stim daca functioneaza


    @classmethod
    def start_client(cls):
        client.Client.__init__()
        cls.thread = threading.Thread(target=client.Client.client_connect)
        cls.thread.start()

        print('Connecting to the server...')
        cls.button_connect.place_forget()
        cls.button_disconnect.place(x=531, y=0)

        cls.print_message("Connected to the server!")

    @classmethod
    def close_client(cls):
        client.Client.client_disconnect()

        print('Disconnecting from the server...')
        cls.button_disconnect.place_forget()
        cls.button_connect.place(x=531, y=0)
        cls.print_message("Disconnected from the server!")

    @classmethod
    def exit(cls):
        cls.window.destroy()

    @classmethod
    def clear_screen(cls):
        print('--Clearing Screen')
        cls.text_box.config(state=NORMAL)
        cls.text_box.delete(1.0, "end")

    @classmethod
    def send_message(cls):
        cls.text_box2.config(state=NORMAL)

        keyboard_input = cls.text_box2.get("1.0", END)
        rezultat = " ".join(keyboard_input.split())
        rezultat = rezultat.split(" ")
        new_str = ""

        for x in range(1, len(rezultat)):
            new_str = new_str + rezultat[x] + " "

        if rezultat[0] not in ("cwd", "ls", "mkdir", "rename"):
            cls.print_message("Introduceti o comanda valida")

        # settere pentru cls.response_message

        cls.response_message.send_to_server(rezultat[0], new_str)

        cls.text_box2.delete(1.0, "end")



