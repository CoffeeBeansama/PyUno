import pygame as pg

class Game:
    def __init__(self,id):
        self.id = id

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