import pygame as pg
from support import loadSprite
from settings import *

class Ui:
    def __init__(self,clock):
        self.clock = clock
        self.screen = pg.display.get_surface()
        pg.font.init()

        self.font = pg.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf",18)

        self.cardsSize = (80,120)
        self.startingCards = 7
        self.tableSprite = loadSprite("Sprites/Uno Game Assets/Table_2.png",(width,height))
        self.tableSpriteRect = self.tableSprite.get_rect(topleft=(0,0))
        self.blankCard = loadSprite("Sprites/Uno Game Assets/Deck.png",self.cardsSize)

        self.importCardSprites()
    
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
    
    def displayFPS(self):
         fps = self.font.render(f"FPS:{round(self.clock.get_fps())}",True,(255,255,255))
         pos = (630,10)
         self.screen.blit(fps,pos)

    def displayCards(self):
        self.screen.blit(self.blankCard,(100,100))
       

    def renderTableGame(self):
        self.screen.blit(self.tableSprite.convert_alpha(),self.tableSpriteRect)