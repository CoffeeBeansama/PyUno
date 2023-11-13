import pygame as pg
from network import Network
import ast
from player import Player
from camera import CameraGroup
from support import *
from tile import Tile
from interactables import *
from settings import *
from cardUi import CardUi
from colorUi import ColorUi

class Game:
    def __init__(self):

        self.window = pg.display.set_mode((width,height))
        

        self.running = True
        self.FPS = 60
        self.clock = pg.time.Clock()

        
        self.network = Network()
        self.visibleSprites = CameraGroup()
        self.collisionSprites = pg.sprite.Group()
        self.interactableSprites = pg.sprite.Group()

        try:
            self.playerID = int(self.network.getPlayerID())
        except:
            pass
        
        self.playerReady = False
        self.battleBegin = False

        p1Pos = (175,100)
        p2Pos = (287,100)
        self.player = Player(self.playerID,p1Pos if self.playerID == 0  else p2Pos,self.visibleSprites,self.collisionSprites,self.interactableSprites)
        self.player2 = Player(self.playerID+1 if self.playerID == 0 else 0,p2Pos if self.playerID == 0 else p1Pos,self.visibleSprites,self.collisionSprites,self.interactableSprites)

        self.cardUi = CardUi(self.clock,self.playerID,self.playerTurn,self.drawSingleCard)
        self.colorUi = ColorUi(self.setColor)

        self.gameData = {
            "Player" : {},
            "PlayerTurn" : None
        }

        self.tileSize = 16
        self.createMap()
        
        pg.display.set_caption(f"Player {str(self.playerID+1)}")
        
    def createMap(self):
        mapLayouts = {
            MapTiles.Walls: import_csv_layout("Map/wall.csv"),
            MapTiles.InteractableObjects: import_csv_layout("Map/interactableObjects.csv")    
        }

        for style,layout in mapLayouts.items():
            for rowIndex,row in enumerate(layout):
                for columnIndex,column in enumerate(row):
                    if column != "-1":
                        x = columnIndex * self.tileSize
                        y = rowIndex * self.tileSize

                        if style == MapTiles.Walls:
                            Tile((x,y),[self.collisionSprites])

                        if style == MapTiles.InteractableObjects:
                            if column == "chair":
                                Chair((x,y),self.interactableSprites,self.playerIn)


    def setColor(self,color):
        self.game = self.network.send(color)
     
    def playerIn(self):
        self.playerReady = True
        self.game = self.network.send("Ready")
        if self.game.bothPlayersReady():
            self.network.send("Game Begin")
            self.battleBegin = True
            return
    
    def drawSingleCard(self):
        if self.game.getCurrentTurn() == self.playerID:
            if self.game.getCurrentDrawStreak() <= 0:
                self.game = self.network.send("Draw Single Card")
            else:
                self.game = self.network.send("Draw Multiple Cards")

    def playerTurn(self,color,value):
        
        if self.game.getCurrentTurn() == self.playerID:

            if self.game.getCurrentPileCard()[CardData.Value.value] == value and self.game.getCurrentDrawStreak() <= 0:
                self.sendUiEvent(value,color)
                    
            elif self.game.getCurrentPileCard()[CardData.Color.value] == color and self.game.getCurrentDrawStreak() <= 0:
                self.sendUiEvent(value,color)

            elif color == self.game.getCurrrentColor() and self.game.getCurrentDrawStreak() <= 0:
                self.sendUiEvent(value,color)

            elif value == "WildDraw":
                self.gameData["PlayerTurn"] = (value,color)
                self.game = self.network.send("Plus Four")
                self.game = self.network.send(str(self.gameData))
                self.colorUi.renderColours = True

            elif value == "Wild" and self.game.getCurrentDrawStreak() <= 0:
                self.gameData["PlayerTurn"] = (value,color)
                self.game = self.network.send(str(self.gameData))
                self.colorUi.renderColours = True
                
            elif value == "Draw" and self.game.getCurrentDrawStreak() > 0:
                self.gameData["PlayerTurn"] = (value,color)
                self.game = self.network.send("Plus Two")
                self.game = self.network.send(str(self.gameData))

            
            

           
    

    def sendUiEvent(self,value,color):
        if value == "Draw":
            self.gameData["PlayerTurn"] = (value,color)
            self.game = self.network.send("Plus Two")
            self.game = self.network.send(str(self.gameData))
        else:
            self.gameData["PlayerTurn"] = (value,color)
            self.game = self.network.send(str(self.gameData))

                

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()

            self.window.fill("black")
            
            self.game = self.network.send("get")

            if not self.playerReady:
                self.player.update()

            
            if self.game.bothPlayersReady():

                self.cardUi.handleRendering(self.game,self.game.getCurrentTurn(),self.playerID)
                self.cardUi.handleUiEvent()

                self.colorUi.drawColours()
                self.colorUi.handleUiEvent()

            else:
                self.visibleSprites.custom_draw(self.player)
                self.gameData["Player"] = self.player.data
                self.network.send(str(self.gameData))
            
           
            

                
            try:
                match self.playerID:
                    case 0:
                            data = self.game.getPlayerTwoData()
                            self.player2.handlePlayer2Movement(
                                    data[PlayerData.Position.value],
                                    data[PlayerData.FrameIndex.value],
                                    data[PlayerData.State.value])
                    case 1:
                            data = self.game.getPlayerOneData()
                            self.player2.handlePlayer2Movement(
                                    data[PlayerData.Position.value],
                                    data[PlayerData.FrameIndex.value],
                                    data[PlayerData.State.value])
            except:
                pass

            self.cardUi.displayFPS()
            pg.display.update()
            self.clock.tick(self.FPS)




game = Game()
game.run()