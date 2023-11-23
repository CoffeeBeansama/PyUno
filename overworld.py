import pygame as pg
from player import Player
from camera import CameraGroup
from support import *
from tile import Tile
from interactables import *
from settings import MapTiles,PlayerData
from network import Network
from scene import Scene


class OverWorld(Scene):
    def __init__(self,sceneCache,game,gamedata,network,playerID):
        super().__init__(sceneCache,game)
        self.sceneCache =  sceneCache
        self.gameData = gamedata
        self.network = network
        self.playerID = playerID
        self.visibleSprites = CameraGroup()
        self.collisionSprites = pg.sprite.Group()
        self.interactableSprites = pg.sprite.Group()

        self.tileSize = 16
        self.createMap()

        self.black = (0,0,0)
        self.white = (255,255,255)
        self.yellow = (255,0,0)

        self.buttonColor = self.black

        self.font = pg.font.Font(self.fontPath,36)
        self.fontColor = self.black

        p1Pos = (175,100)
        p2Pos = (287,100)
        self.player = Player(self.playerID,p1Pos if self.playerID == 0  else p2Pos,self.visibleSprites,self.collisionSprites,self.interactableSprites)
        self.player2 = Player(self.playerID+1 if self.playerID == 0 else 0,p2Pos if self.playerID == 0 else p1Pos,self.visibleSprites,self.collisionSprites,self.interactableSprites)
        
        self.playerReady = False


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
                                Chair((x,y),self.interactableSprites)

        
        
        
    def getPlayer2Movement(self):
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
    
    def handleEvent(self):
         mousePos = pg.mouse.get_pos()
         mousePressed = pg.mouse.get_pressed()

         if self.readyButton.collidepoint(mousePos):
              self.buttonColor = self.white
              self.fontColor = self.black
              if mousePressed[0]:
                    self.network.send("Ready")
                    self.fontColor = self.yellow
         else:
              self.buttonColor = self.black
              self.fontColor = self.white
              


    def renderReadyButton(self):
         btnX = 530
         btnY = 430
         btnWidth = 150
         btnHeight = 50
         self.readyButton = pg.draw.rect(self.screen,self.buttonColor,(btnX,btnY,btnWidth,btnHeight))

         ready = self.font.render("Ready",True,self.fontColor)
         self.screen.blit(ready,(560,432))
         

    def update(self,game):
        self.game = game
        self.player.update()
        self.visibleSprites.custom_draw(self.player)
        self.renderReadyButton()
        self.handleEvent()
        

        
            

        self.gameData["Player"] = self.player.data
        self.network.send(str(self.gameData))
        self.getPlayer2Movement()

        if self.game.bothPlayersReady():
            self.switchScene(self.sceneCache.gameTable())
            