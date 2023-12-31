import pygame as pg
from cardUi import CardUi
from colorUi import ColorUi
from unoUi import UnoUi
from settings import CardData,width,height
from scene import Scene
from support import loadSprite
from timer import Timer

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

        self.initializeBackgroundImage()
        
        self.initializeVisualEffect()

    
    def initializeBackgroundImage(self):
        self.tableSprite = loadSprite("Sprites/Uno Game Assets/Table_2.png",(width,height)).convert_alpha()
        self.tableSpriteRect = self.tableSprite.get_rect(topleft=(0,0))

    def initializeVisualEffect(self):
        self.effectAnimate = False
        self.circleColor = (255,255,255)
        self.circlePos = [340,250]
        self.circleRadius = 0
        self.circleWidth = 13

        self.effectTimer = Timer(1500,self.resetVisualEffect)

    def setColor(self,color):
        self.game = self.network.send(color)
        
    def drawSingleCard(self):
        if self.game.getCurrentTurn() == self.playerID:
            if self.game.getCurrentDrawStreak() <= 0:
                self.game = self.network.send("Draw Single Card")
            else:
                self.game = self.network.send("Draw Multiple Cards")

    def cardWithSameAttribute(self,value,color):
        if self.game.getCurrentPileCard()[CardData.Value.value] == value:
            return True
        if self.game.getCurrentPileCard()[CardData.Color.value] == color:
            return True
        if color == self.game.getCurrrentColor():
            return True
        return False

    def playerTurn(self,color,value):
        if self.game.getCurrentTurn() == self.playerID:
            if self.game.getCurrentDrawStreak() <= 0:
                if self.cardWithSameAttribute(value,color):
                    self.sendUiEvent(value,color)
                if value == "Wild":
                    self.colorUi.renderColours = True
                    self.sendUiEvent(value,color)
            else:
                if value == "Draw":
                    self.playerData["PlayerTurn"] = (value,color)
                    self.game = self.network.send("Plus Two")
                    self.game = self.network.send(str(self.playerData))
                    self.effectAnimate = True

            if value == "WildDraw":
                    self.game = self.network.send("Plus Four")
                    self.colorUi.renderColours = True
                    self.sendUiEvent(value,color)
                    self.effectAnimate = True
                

    def sendUiEvent(self,value,color):
        if value == "Draw":
            self.playerData["PlayerTurn"] = (value,color)
            self.game = self.network.send("Plus Two")
            self.game = self.network.send(str(self.playerData))
            self.effectAnimate = True
        else:
            self.playerData["PlayerTurn"] = (value,color)
            self.game = self.network.send(str(self.playerData))

    def handleVisualEffect(self):
        if not self.effectAnimate: return

        if not self.effectTimer.activated:
            self.effectTimer.activate()
        
        self.circleRadius += 14
        pg.draw.circle(self.screen,self.circleColor,self.circlePos,self.circleRadius,self.circleWidth)

        
    
    def resetVisualEffect(self):
        self.circleRadius = 0
        self.effectAnimate = False

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
        self.effectTimer.update()
        self.screen.blit(self.tableSprite,self.tableSpriteRect)

        self.cardUi.update(self.game,self.game.getCurrentTurn(),self.playerID)
        self.colorUi.update()
        
        if self.checkPlayerUno():
            if not self.game.gameUno():
                self.unoUi.renderUno()


        if self.game.playerWon() is not None:
            thisPlayerWon = self.game.playerWon() == self.playerID
            if thisPlayerWon:
                self.cardUi.renderPlayerWon(thisPlayerWon)
            else:
                self.cardUi.renderPlayerWon(thisPlayerWoin)

        self.handleVisualEffect()
