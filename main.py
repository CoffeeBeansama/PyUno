import pygame as pg
from network import Network
import ast
from player import Player
from camera import CameraGroup
from support import *
from tile import Tile
from enum import Enum
from interactables import *

class MapTiles(Enum):
    Walls = 1
    InteractableObjects = 2

class Game:
    def __init__(self):
        self.window = pg.display.set_mode((700,500))
    
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

        self.gameData = {
            "Player" : {},
            
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
        self.network.send("Ready")
                
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
                self.battleBegin = True
            
            if not self.battleBegin:
                self.visibleSprites.custom_draw(self.player)

            self.gameData["Player"] = self.player.data
            
            self.network.send(str(self.gameData))

            
            match self.playerID:
                case 0:
                    if type(self.game.getPlayerTwoData()) == str:
                        data = ast.literal_eval(str(self.game.getPlayerTwoData()))
                        playerData = data["Player"]
                        self.player2.handlePlayer2Movement(playerData["Pos"],playerData["FrameIndex"],playerData["State"])
                case 1:
                    if type(self.game.getPlayerOneData()) == str:
                        data = ast.literal_eval(str(self.game.getPlayerOneData()))
                        playerData = data["Player"]
                        self.player2.handlePlayer2Movement(playerData["Pos"],playerData["FrameIndex"],playerData["State"])
                        
            pg.display.update()
            self.clock.tick(self.FPS)




game = Game()
game.run()