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
    text_box = None
    text_box2 = None
    server_ip = None
    server_port = None
    client_ip = None
    client_port = None
    text_server = None

    @classmethod
    def __init__(cls):
        cls.received_message = CoAP.Message.Message('Server')
        cls.response_message = CoAP.Message.Message('Client')
        cls.server_ip = 0
        cls.server_port = 0
        cls.client_ip = 0
        cls.client_port = 0

        cls.window = Tk()

        cls.button_connect = Button(cls.window, height=2, width=14, text="Connect", font="arial 15 bold",
                                    bg="#98fb98", command=cls.start_client)
        cls.button_disconnect = Button(cls.window, height=2, width=14, text="Disconnect", font="arial 15 bold",
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
        cls.text_box_connect_server = Text(cls.window, height=1, width=13,font="arial 10", bg="#eeeeee")
        cls.text_box_connect_client = Text(cls.window, height=1, width=13,font="arial 10", bg="#eeeeee")
        cls.text_server = Label(cls.window, text = "Server").place(x = 531, y = 1)
        cls.text_client = Label(cls.window, text="Client").place(x=531, y=23)
    @classmethod
    def start_application(cls):
        cls.window.wm_title('Browser CoAP')
        cls.window.geometry("750x500")

        cls.button_connect.place(x=531, y=45)
        cls.button_confirmable.place(x=531, y=115)
        cls.button_clearScreen.place(x=531, y=210)
        cls.button_exit.place(x=531, y=305)
        cls.button_send.place(x=531, y=410)
        cls.text_box.place(x=0, y=0)
        cls.text_box2.place(x=0, y=400)
        cls.text_box_connect_server.place(x=613, y=1)
        cls.text_box_connect_client.place(x=613, y=23)
        cls.text_box_connect_server.insert(1.0, "127.0.0.1:2001")
        cls.text_box_connect_client.insert(1.0, "127.0.0.2:2000")
        cls.window.mainloop()

    @classmethod
    def print_message(cls, message):
        cls.text_box.config(state=NORMAL)
        cls.text_box.insert(END, ">> " + message + "\n")
        cls.text_box.config(state=DISABLED)

    @classmethod
    def print_comenzi(cls, message):
        cls.text_box.config(state=NORMAL)
        cls.text_box.insert(END, "" + message + "\n")
        cls.text_box.config(state=DISABLED)

    @classmethod
    def get_ip_port_server(cls):
        cls.text_box_connect_server.config(state=NORMAL)
        keyboard_input = cls.text_box_connect_server.get("1.0", END)
        ip_port = " ".join(keyboard_input.split())
        ip_port = ip_port.split(":")
        server_ip = ip_port[0]
        server_prt = ip_port[1]
        cls.server_ip = str(server_ip)
        cls.server_port = int(server_prt)
        print(server_ip, server_prt)

    @classmethod
    def get_ip_port_client(cls):
        cls.text_box_connect_client.config(state=NORMAL)
        keyboard_input = cls.text_box_connect_client.get("1.0", END)
        ip_port = " ".join(keyboard_input.split())
        ip_port = ip_port.split(":")
        client_ip = ip_port[0]
        client_prt = ip_port[1]
        cls.client_ip = str(client_ip)
        cls.client_port = int(client_prt)
        print(client_ip, client_prt)

    @classmethod
    def non_conf(cls):
        cls.button_non_confirmable.place_forget()
        cls.button_confirmable.place(x=531, y=115)
        cls.print_message("Using confirmable")
        cls.response_message.set_msg_type(0)
        # nu stim daca functioneaza

    @classmethod
    def conf(cls):
        cls.button_confirmable.place_forget()
        cls.button_non_confirmable.place(x=531, y=115)
        cls.print_message("Using non_confirmable")
        cls.response_message.set_msg_type(1)
        # nu stim daca functioneaza


    @classmethod
    def start_client(cls):
        cls.get_ip_port_server()
        cls.get_ip_port_client()

        client.Client.__init__()
        cls.thread = threading.Thread(target=client.Client.client_connect)
        cls.thread.start()

        print('Connecting to the server...')
        cls.button_connect.place_forget()
        cls.button_disconnect.place(x=531, y=45)

        cls.print_message("Connected to the server!")
        cls.print_comenzi("\tAvailable commands:")
        cls.print_comenzi("- ls")
        cls.print_comenzi("- cwd")
        cls.print_comenzi("- newDir dirName")
        cls.print_comenzi("- newFile fileName")
        cls.print_comenzi("- move newLocation fileName -> You have to be in the directory where 'fileName' is")
        cls.print_comenzi("- delete name")
        cls.print_comenzi("- rename oldName newName")

    @classmethod
    def close_client(cls):
        client.Client.client_disconnect()

        print('Disconnecting from the server...')
        cls.button_disconnect.place_forget()
        cls.button_connect.place(x=531, y=45)
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
        if len(rezultat) == 1:
            pass
        else:
            for x in range(1, len(rezultat)-1):
                new_str = new_str + rezultat[x] + " "
            new_str = new_str + rezultat[len(rezultat)-1]
            #print("c"+new_str+"c")

        if rezultat[0] not in ("", "chdir", "cwd", "newDir", "newFile", "ls", "rename", "move", "delete"):
            cls.print_message("Introduceti o comanda valida!!")

        # settere pentru cls.response_message
        if rezultat[0] in ['cwd', 'ls']:
            cls.response_message.set_msg_class(0)
            cls.response_message.set_msg_code(1)
        elif rezultat[0] in ['newDir', 'newFile', 'chdir']:
            cls.response_message.set_msg_class(0)
            cls.response_message.set_msg_code(2)
        elif rezultat[0] == 'move':
            cls.response_message.set_msg_class(0)
            cls.response_message.set_msg_code(3)
        elif rezultat[0] == 'delete':
            cls.response_message.set_msg_class(0)
            cls.response_message.set_msg_code(4)
        elif rezultat[0] == 'rename':
            cls.response_message.set_msg_class(0)
            cls.response_message.set_msg_code(8)
        elif rezultat[0] == '':
            cls.response_message.set_msg_class(0)
            cls.response_message.set_msg_code(0)
            cls.response_message.set_payload_marker(0)

        CoAP.Client.Client.send_to_server(rezultat[0], new_str, cls.response_message)

        cls.text_box2.delete(1.0, "end")



