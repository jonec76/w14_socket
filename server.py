import socket
import threading
from color import bcolors

class Server:
    def __init__(self):
        self.start_server()
    def start_server(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
       
        host = "0.0.0.0"
        port = 8765

        self.clients = []
        self.threads = []
        self.s.bind((host,port))
        self.s.listen(100)
    
        print('Running on host: '+str(host))
        print('Running on port: '+str(port))

        self.username_lookup = {}

        while True:
            try:
                c, addr = self.s.accept()
                username = c.recv(1024).decode()
                print('New connection. Username: '+str(username))
                self.broadcast('New person joined the room. Username: '+username)

                self.username_lookup[c] = username

                self.clients.append(c)
                
                self.threads.append(threading.Thread(target=self.handle_client,args=(c,addr,)).start())
            except:
                self.broadcast("Server is closed")
                for c in self.clients:
                    c.shutdown(socket.SHUT_RDWR)

                for t in self.threads:
                    if t:
                        t.join()
                self.s.close()
                break

    def broadcast(self,msg):
        pass

    def handle_client(self, c, addr):
        while True:
            msg = c.recv(1024)
            if msg.decode() != '':
                msg = bcolors.OKGREEN + str(self.username_lookup[c])+" : " + str(msg.decode()) + bcolors.ENDC
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg.encode())
            else:
                # c.shutdown(socket.SHUT_RDWR)
                if c:
                    self.clients.remove(c)
                print(str(self.username_lookup[c])+' left the room.')
                self.broadcast(str(self.username_lookup[c])+' has left the room.')
                break

server = Server()