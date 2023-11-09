import pygame as pg
from network import Network
import ast
from player import Player
from camera import CameraGroup
from support import *
from tile import Tile
from interactables import *
from settings import *
from ui import Ui


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

        
        self.ui = Ui(self.clock,self.playerID,self.playerTurn)
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


    def playerIn(self):
        self.playerReady = True
        self.game = self.network.send("Ready")
        if self.game.bothPlayersReady():
            self.network.send("Game Begin")
            self.battleBegin = True
            return
       
    def playerTurn(self,color,value):
        
        if self.game.getCurrentTurn() == self.playerID:
    
            if value in ["Wild", "WildDraw"]:
                self.gameData["PlayerTurn"] = (value,color)
                self.game = self.network.send(str(self.gameData))
            elif self.game.getCurrentPileCard()[CardData.Color.value] == color:
                self.gameData["PlayerTurn"] = (value,color)
                self.game = self.network.send(str(self.gameData))
            elif self.game.getCurrentPileCard()[CardData.Value.value] == value:
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
                self.ui.handleRendering(self.game)
                self.ui.handleUiEvent()
                
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

            self.ui.displayFPS()
            pg.display.update()
            self.clock.tick(self.FPS)




game = Game()
game.run()