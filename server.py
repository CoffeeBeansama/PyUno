import socket
from _thread import *
import pickle
from gamedata import Game
from settings import port


class Server:
    def __init__(self):

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        self.server = ip_address

        self.port = port
        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.gameIdCount = 0

        self.games = {}
        self.idCount = 0

        self.startServer()

        self.currentPlayers = 0

        

    def startServer(self):
        try:
            self._socket.bind((self.server,self.port))
        except socket.error as e:
            pass

        self._socket.listen()
        print("Waiting for connection...Server started!")

    def threadedClient(self,conn,player,playerID):
        conn.send(str.encode(str(player)))

        while True:
            try:
                data = conn.recv(4096).decode()
                if playerID in self.games:
                    game = self.games[playerID]
                    if not data:
                        break
                    else:
                        if data != "get":
                           game.processData(player,data)
                           
                        conn.sendall(pickle.dumps(game))

                else: break
            except: break
                
        try: 
            del self.games[playerID]
            
        except: pass
            
        self.idCount -= 1
        conn.close()
  
    
    def run(self):
        while True:
            conn,addr = self._socket.accept()

            self.idCount += 1
            player = 0
            gameId = (self.idCount -1) // 2

            if self.idCount % 2 == 1:
                self.games[gameId] = Game(gameId)
            else:
                player = 1

            
            start_new_thread(self.threadedClient,(conn,player,gameId))
           




server = Server()
server.run()