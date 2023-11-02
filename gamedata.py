import pygame as pg

class Game:
    def __init__(self,id):
        self.id = id
        
        self.playersReady = [False,False]

        self.data = {
            "PlayerOne" : None,
            "PlayerTwo" : None
        }

        

            
    def updatePlayerOneData(self,data):
        self.data["PlayerOne"] = data
        
    def updatePlayerTwoData(self,data):
        self.data["PlayerTwo"] = data

    def getPlayerOneData(self):
        return self.data["PlayerOne"]
    
    def getPlayerTwoData(self):
        return self.data["PlayerTwo"]
    
    def playerReady(self,player):
        match player:
            case 0:
                self.playersReady[0] = True
            case 1:
                self.playersReady[1] = True

    

    def bothPlayersReady(self):
        if self.playersReady[0] and self.playersReady[1]:
            return True
        
        return False