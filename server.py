import socket
from _thread import *
import pickle
from gamedata import Game


class Server:
    def __init__(self):

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        self.server = ip_address

        self.port = 5558
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

    def threadedClient(self,conn,player,gameId):
        conn.send(str.encode(str(player)))

        reply = ""
        while True:
            try:
                data = conn.recv(4096).decode()
                if gameId in self.games:
                    game = self.games[gameId]
                    if not data:
                        break
                    else:
                        if data != "get":
                           if data == "Ready":
                                game.playerReady(player)
                           if data == "Game Begin":
                               game.roundBegin()
                           else:
                                if player == 0:
                                    game.updatePlayerOneData(data)
                                if player == 1:
                                    game.updatePlayerTwoData(data)
                           
                        conn.sendall(pickle.dumps(game))
                else:
                    break
            except:
                
                break
        print("Lost connection")

        try:
            del self.games[gameId]
        except:
            
            pass
        
        self.idCount -= 1
        conn.close()
        
        print("Connection lost")
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