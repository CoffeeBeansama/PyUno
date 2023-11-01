import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        self.server = ip_address
        self.port = 5559
        self.addr = (self.server,self.port)
        self.player = self.connect()

    def getPlayerID(self):
        return self.player
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4068).decode()
        except:
            pass

    def send(self,data):
        try:
            self.client.send(str.encode(data))  
            return pickle.loads(self.client.recv(4068))
        except socket.error as e:
            pass