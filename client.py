import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 9090


class Client:

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring(
            "Nickname", "Choose your nickname:", parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):

        self.win = tkinter.Tk()
        self.win.title("Chat")
        self.win.configure(bg="#1a1a1a")
        self.win.geometry("525x525")

        # Messages area
        self.chat_label = tkinter.Label(
            self.win, text="Chat:", font=("Helvetica", 15), bg="#1a1a1a", fg="white")
        self.chat_label.pack(pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(
            self.win, height=20, width=50, bg="#252525", fg="white")
        self.text_area.pack(padx=20, pady=5)

        # Input area
        self.msg_label = tkinter.Label(
            self.win, text="Message:", font=("Arial", 14), bg="#1a1a1a", fg="white")
        self.msg_label.pack(pady=5)

        self.input_area = tkinter.Text(
            self.win, height=3, width=50, bg="#252525", fg="white")
        self.input_area.pack(padx=20, pady=5)

        # Send button
        self.send_button = tkinter.Button(
            self.win, text="Send", font=("Arial", 14), bg="#363636", fg="white", command=self.write)
        self.send_button.pack(pady=5)

        self.gui_done = True

        # Close window event
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0' , 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        if message.startswith(self.nickname):
                            self.text_area.tag_configure(
                                'client', foreground='#00bfff')
                            self.text_area.insert('end', message, 'client')
                        else:
                            self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disable')

            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break


client = Client(HOST, PORT)
