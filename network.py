import socket
import pickle
from settings import port

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        self.server = ip_address
        self.port = port
        self.addr = (self.server,self.port) # this one
        self.connectPlayer()
        

    def getPlayerID(self):
        return self.player
    
    def connectPlayer(self):
        self.connected = True
        self.player = self.connect()
       

    def disconnectPlayer(self):
        self.connected = False

    def connect(self):
        try: 
            self.client.connect(self.addr)
            return self.client.recv(4096).decode()
        except:
            pass

    def send(self,data):
        try:
            if self.connected:
                self.client.send(str.encode(data))  
                return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            
            pass