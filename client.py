import socket
import threading
import sys
import signal

def colored(text, r=0, g=255, b=128):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

class Client:
    def __init__(self):
        self.create_connection()
    def create_connection(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        while 1:
            try:
                host = "0.0.0.0"
                port = 8765
                self.s.connect((host,port))
                break
            except:
                print("Couldn't connect to server")
                break

        self.username = input('Enter username: ')
        self.s.send(self.username.encode())
        
        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler,args=())
        input_handler.start()

    def handle_messages(self):
        while 1:
            recv = self.s.recv(1204).decode()
            if recv == "":
                self.s.close()
                sys.exit(0)
            
            print(recv)
    def input_handler(self):
        while 1:
            try:
                # self.s.send((self.username+' : '+input()).encode())
                self.s.send((input()).encode())
            except KeyboardInterrupt:
                break
            except:
                print("Can't send to server")
                break

client = Client()