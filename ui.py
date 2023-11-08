import pygame as pg
from support import loadSprite
from settings import *
from timer import Timer

class Ui:
    def __init__(self,clock,playerID,playerTurn):
        self.clock = clock
        self.playerID = playerID
        self.playerTurn = playerTurn
        self.screen = pg.display.get_surface()
        pg.font.init()

        self.font = pg.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf",18)

        self.cardsSize = (80,120)
        self.startingCards = 7
        self.tableSprite = loadSprite("Sprites/Uno Game Assets/Table_2.png",(width,height)).convert_alpha()
        self.tableSpriteRect = self.tableSprite.get_rect(topleft=(0,0))
        self.blankCard = loadSprite("Sprites/Uno Game Assets/Deck.png",self.cardsSize).convert_alpha()

        self.playerDeck = {}

        self.playerDeckBG = loadSprite("Sprites/playerDeckBg.png",(660,150))
        self.playerDeckBG_Rect = self.playerDeckBG.get_rect(topleft=(20,340))
        self.playerDeckBG.set_alpha(120)
        self.cardDeckWidth = 625
        self.p1DeckPosY = 355
        
        self.player2DeckBG = self.playerDeckBG
        self.player2DeckBG_Rect = self.player2DeckBG.get_rect(topleft=(20,10))
        self.player2DeckBG.set_alpha(120)
        self.p2DeckPosY = 20

        self.wildCards = ["Wild","WildDraw"]
        self.colorCards = ["0","1","2","3","4","5","6","7","8","9","Draw","Reverse","Skip"]
        
        self.transitionSprite = loadSprite("Sprites/playerDeckBg.png",(width,height)).convert_alpha()
        self.transitionSpriteRect = self.transitionSprite.get_rect(topleft=(0,0))
        self.transitionSprite.set_alpha(0)
        self.transitioned = False

        self.importCardSprites()

        self.timer = Timer(300)
    
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
        for sprites in self.colorCards:
            self.cardSprites[color][sprites] = loadSprite(f"{self.cardSpritePath}{color}/{color}_{sprites}.png",(80,120)).convert_alpha()

        
    def getWildCards(self,color):
        for sprites in self.wildCards:
            self.cardSprites[color][sprites] = loadSprite(f"{self.cardSpritePath}{color}/{sprites}.png",(80,120)).convert_alpha()
    
    def displayFPS(self):
         fps = self.font.render(f"{round(self.clock.get_fps())}",True,(255,255,255))
         pos = (670,10)
         self.screen.blit(fps,pos)

    def displayCards(self):
        self.screen.blit(self.blankCard,(100,100))
       
    
    def handleUiEvent(self):
        self.timer.update()
        mousePos = pg.mouse.get_pos()
        mousePressed = pg.mouse.get_pressed()

        try:
            for data,cardsUi in self.playerDeck.items():
                   if cardsUi.collidepoint(mousePos) and not self.timer.activated:
                        if mousePressed[0]:
                            self.playerTurn(data[0],data[1])
                            self.timer.activate()
        except:
            pass

    def handleRendering(self,game):
        
        self.screen.blit(self.tableSprite,self.tableSpriteRect)
        self.screen.blit(self.playerDeckBG,self.playerDeckBG_Rect)
        self.screen.blit(self.player2DeckBG,self.player2DeckBG_Rect)

        try:
            self.currentPileCard = game.pile[0]
            self.screen.blit(self.cardSprites[self.currentPileCard[CardData.Color.value]][str(self.currentPileCard[0])],(300,190))
            self.screen.blit(self.blankCard,(410,190))

            
            playerDeckSize : int = len(game.player1Deck if self.playerID == 0 else game.player2Deck)
            for i in range(playerDeckSize):

                lenghtDistance = self.playerDeckBG_Rect.y // playerDeckSize
                lengthIncrement = self.cardDeckWidth // playerDeckSize
                x = (i * lengthIncrement) + (lengthIncrement - lenghtDistance)

                playerCardColours = game.player1Deck[i][CardData.Color.value] if self.playerID == 0 else game.player2Deck[i][CardData.Color.value]
                playerCardValues = str(game.player1Deck[i][CardData.Value.value]) if self.playerID == 0 else str(game.player2Deck[i][CardData.Value.value])
                
                self.playerDeck[(playerCardColours,playerCardValues)] = self.screen.blit(self.cardSprites[playerCardColours][playerCardValues],
                                (x,self.p1DeckPosY))
                
            
            player2DeckSize : int = len(game.player1Deck if self.playerID == 1 else game.player2Deck)
            for j in range(player2DeckSize):

                lenghtDistance = self.playerDeckBG_Rect.y // player2DeckSize
                lengthIncrement = self.cardDeckWidth // player2DeckSize
                x = (j * lengthIncrement) + (lengthIncrement - lenghtDistance)

                self.screen.blit(self.blankCard,(x,self.p2DeckPosY))

            
        except:
            pass

        
        

            
