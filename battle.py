import pygame as pg
from cardUi import CardUi
from colorUi import ColorUi
from unoUi import UnoUi
from settings import CardData
from scene import Scene

class GameTable(Scene):
    def __init__(self,sceneCache,game,playerData,network,playerID):
        super().__init__(sceneCache,game)
        
        self.sceneCache = sceneCache
        self.network = network
        self.playerID = playerID
        
        self.playerData = playerData

        self.playerReady = False
        self.battleBegin = False

        self.cardUi = CardUi(self.playerID,self.playerTurn,self.drawSingleCard)
        self.colorUi = ColorUi(self.setColor)
        self.unoUi = UnoUi(self.calledUno)

    def setColor(self,color):
        self.game = self.network.send(color)
    
    
    def drawSingleCard(self):
        if self.game.getCurrentTurn() == self.playerID:
            if self.game.getCurrentDrawStreak() <= 0:
                self.game = self.network.send("Draw Single Card")
            else:
                self.game = self.network.send("Draw Multiple Cards")

    def playerTurn(self,color,value):
        if self.game.getCurrentTurn() == self.playerID:
            
            if self.game.getCurrentDrawStreak() <= 0:
                isSameAttribute = self.game.getCurrentPileCard()[CardData.Value.value] == value or self.game.getCurrentPileCard()[CardData.Color.value] == color or color == self.game.getCurrrentColor()

                if isSameAttribute:
                    self.sendUiEvent(value,color)

                elif value == "Wild":
                    self.playerData["PlayerTurn"] = (value,color)
                    self.game = self.network.send(str(self.playerData))
                    self.colorUi.renderColours = True
                    self.sendUiEvent(value,color)
            else:
                if value == "Draw":
                    self.playerData["PlayerTurn"] = (value,color)
                    self.game = self.network.send("Plus Two")
                    self.game = self.network.send(str(self.playerData))
                    
            if value == "WildDraw":
                    self.playerData["PlayerTurn"] = (value,color)
                    self.game = self.network.send("Plus Four")
                    self.game = self.network.send(str(self.playerData))
                    self.colorUi.renderColours = True
                    self.sendUiEvent(value,color)

    def sendUiEvent(self,value,color):
        if value == "Draw":
            self.playerData["PlayerTurn"] = (value,color)
            self.game = self.network.send("Plus Two")
            self.game = self.network.send(str(self.playerData))
        else:
            self.playerData["PlayerTurn"] = (value,color)
            self.game = self.network.send(str(self.playerData))
    
    def checkPlayerUno(self):
        player1DeckSize : int = len(self.game.player1Deck if self.playerID == 0 else self.game.player2Deck)
        player2DeckSize : int = len(self.game.player1Deck if self.playerID == 1 else self.game.player2Deck)
        if player1DeckSize == 1 or player2DeckSize == 1:
            return True
        return False
    
    def calledUno(self):
        self.game = self.network.send("Called Uno")
    
    
    def update(self,game):
        
        self.game = game
        self.cardUi.handleRendering(self.game,self.game.getCurrentTurn(),self.playerID)
        self.cardUi.handleUiEvent()

        self.colorUi.drawColours()
        self.colorUi.handleUiEvent()
                
        if self.checkPlayerUno():
            if not self.game.gameUno():
                self.unoUi.renderUno()

        if self.game.playerWon() is not None:
            thisPlayerWon = self.game.playerWon() == self.playerID
            if thisPlayerWon:
                self.cardUi.renderPlayerWon(thisPlayerWon)
            else:
                self.cardUi.renderPlayerWon(thisPlayerWon)