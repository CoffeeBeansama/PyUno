import pygame as pg
from network import Network
import ast
from player import Player
from camera import CameraGroup
from support import *
from tile import Tile
from interactables import *
from settings import *


class Game:
    def __init__(self):

        width,height = 700,500
        self.window = pg.display.set_mode((width,height))
        pg.font.init()

        self.font = pg.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf",18)
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

        self.cardsSize = (80,120)
        self.startingCards = 7
        self.tableSprite = loadSprite("Sprites/Uno Game Assets/Table_2.png",(width,height))
        self.tableSpriteRect = self.tableSprite.get_rect(topleft=(0,0))
        self.blankCard = loadSprite("Sprites/Uno Game Assets/Deck.png",self.cardsSize)

        self.gameData = {
            "Player" : {},
            
        }

        self.tileSize = 16
        self.createMap()
        self.importCardSprites()
        pg.display.set_caption(f"Player {str(self.playerID+1)}")
        

    def importCardSprites(self):

        self.cardSpritePath = "Sprites/Uno Game Assets/"
        self.cardSprites = {
            "Blue" : {} ,"Red" : {}, "Yellow": {}, "Green": {},
            "WildCards": {}
        }

        self.getColorCards("Blue")
        self.getColorCards("Red")
        self.getColorCards("Yellow")
        self.getColorCards("Green")
        self.getWildCards("WildCards")

    def getColorCards(self,color):
        for sprites in colorCards:
            self.cardSprites[color][sprites] = loadSprite(f"{self.cardSpritePath}{color}/{color}_{sprites}.png",(80,120))

    def getWildCards(self,color):
        for sprites in wildCards:
            self.cardSprites[color][sprites] = loadSprite(f"{self.cardSpritePath}{color}/{sprites}.png",(80,120))

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
       
    def displayFPS(self):
         fps = self.font.render(f"FPS:{round(self.clock.get_fps())}",True,(255,255,255))
         pos = (630,10)
         self.window.blit(fps,pos)

    def displayCards(self):
        self.window.blit(self.blankCard,(100,100))
        pass

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
                self.window.blit(self.tableSprite.convert_alpha(),self.tableSpriteRect)
            else:
                self.visibleSprites.custom_draw(self.player)

            
            self.gameData["Player"] = self.player.data
            
            self.network.send(str(self.gameData))

            try:
                match self.playerID:
                    case 0:
                        if type(self.game.getPlayerTwoData()) == str:
                            data = ast.literal_eval(str(self.game.getPlayerTwoData()))
                            playerData = data["Player"]
                            self.player2.handlePlayer2Movement(
                                playerData[PlayerData.Position.value],
                                playerData[PlayerData.FrameIndex.value],
                                playerData[PlayerData.State.value])
                    case 1:
                        if type(self.game.getPlayerOneData()) == str:
                            data = ast.literal_eval(str(self.game.getPlayerOneData()))
                            playerData = data["Player"]
                            self.player2.handlePlayer2Movement(
                                playerData[PlayerData.Position.value],
                                playerData[PlayerData.FrameIndex.value],
                                playerData[PlayerData.State.value])
                        
            except:
                pass

            self.displayFPS()
            pg.display.update()
            self.clock.tick(self.FPS)




game = Game()
game.run()