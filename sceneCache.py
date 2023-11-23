from overworld import OverWorld
from menu import MainMenu
from lobby import Lobby
from battle import GameTable

class SceneCache:
    def __init__(self,game):
        self.game = game

        self.scenes = {
            "Main Menu" : MainMenu(self,self.game),
            "Lobby" : Lobby(self,self.game),
            "Game" : GameTable(self,self.game,self.game.playerData,self.game.network,self.game.playerID),
            "OverWorld" : OverWorld(self,self.game,self.game.playerData,self.game.network,self.game.playerID),
        }

        

    def mainMenu(self):
        return self.scenes["Main Menu"]
    
    def lobby(self):
        return self.scenes["Lobby"]
    
    def overWorld(self):
        return self.scenes["OverWorld"]
    
    def gameTable(self):
        return self.scenes["Game"]
