import pygame as pg
from support import loadSprite
from settings import *
from timer import Timer


class CardUi:
    def __init__(self,clock,playerID,playerTurn,drawSingleCard,playerUno):
        self.screen = pg.display.get_surface()
        pg.font.init()

        self.clock = clock
        self.playerID = playerID
        self.playerTurn = playerTurn
        self.drawSingleCard = drawSingleCard
        self.playerUno = playerUno


        self.font = pg.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf",18)

        self.cardsSize = (80,120)
        self.startingCards = 7
        self.tableSprite = loadSprite("Sprites/Uno Game Assets/Table_2.png",(width,height)).convert_alpha()
        self.tableSpriteRect = self.tableSprite.get_rect(topleft=(0,0))
        self.blankCard = loadSprite("Sprites/Uno Game Assets/Deck.png",self.cardsSize).convert_alpha()

        self.playerDeckCards = {}
      

        self.playerDeckBG = loadSprite("Sprites/playerDeckBg.png",(660,150))
        self.playerDeckBG_Rect = self.playerDeckBG.get_rect(topleft=(20,340))
        self.playerDeckBG.set_alpha(240)
        
        self.cardDeckWidth = 625
        self.p1DeckPosY = 355
        
        self.player2DeckBG = self.playerDeckBG
        self.player2DeckBG_Rect = self.player2DeckBG.get_rect(topleft=(20,10))
        
        self.p2DeckPosY = 20

        self.wildCards = ["Wild","WildDraw"]
        self.colorCards = ["0","1","2","3","4","5","6","7","8","9","Draw","Reverse","Skip"]
        
        self.transitionSprite = loadSprite("Sprites/playerDeckBg.png",(width,height)).convert_alpha()
        self.transitionSpriteRect = self.transitionSprite.get_rect(topleft=(0,0))
        self.transitionSprite.set_alpha(0)
        self.transitioned = False


        self.importCardSprites()

        self.timer = Timer(300)

        
        self.renderColours = False

        self.drawCard = self.screen.blit(self.blankCard,(410,190))


        self.blue = None
        self.green = None
        self.red = None
        self.yellow = None


        self.colorSize = 150

        self.playerDeckBGX = 15
        self.playerDeckBGY = 335

        self.player2DeckBGX = 15
        self.player2DeckBGY = 5

        self.deckBGWidth = 670
        self.deckBGHeight = 160

        self.deletedCard = None

        self.unoSprite = loadSprite("Sprites/Uno.png",(150,90)).convert_alpha()
        self.unoSpriteRect = self.unoSprite.get_rect(topleft=(540,200))

        self.unoUi = self.screen.blit(self.unoSprite,self.unoSpriteRect)

       
    def importCardSprites(self):
        self.cardSpritePath = "Sprites/Uno Game Assets/"

        self.cardSprites = {
            "Blue" : {} ,"Red" : {}, "Yellow": {}, "Green": {},
            "WildCards": {}
        }

        self.cardSpriteMask = {
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

        for data,cardsUi in self.playerDeckCards.items():
            if cardsUi.collidepoint(mousePos):
                if mousePressed[0]:
                    if not self.timer.activated:
                        self.playerTurn(data[0],data[1])
                        self.deletedCard = data
                        self.timer.activate()
        
    
        if self.deletedCard is not None:
            if self.deletedCard in self.playerDeckCards.keys():
                del self.playerDeckCards[self.deletedCard]
                self.deletedCard = None    
                

        if self.drawCard.collidepoint(mousePos):
            if mousePressed[0]:
                if not self.timer.activated:
                    self.drawSingleCard()
                    self.timer.activate()
                    

    def renderUno(self):
        mousePos = pg.mouse.get_pos()
        mousePressed = pg.mouse.get_pressed()

        self.unoUi = self.screen.blit(self.unoSprite,self.unoSpriteRect)

        
        if self.unoUi.collidepoint(mousePos):
            if mousePressed[0]:
                if not self.timer.activated:
                    self.playerUno()
                    self.timer.activate()

        

    def handleRendering(self,game,turn,playerID):
        self.timer.update()
        self.screen.blit(self.tableSprite,self.tableSpriteRect)

        if turn == playerID:
            pg.draw.rect(self.screen,(255,255,255),(self.playerDeckBGX,self.playerDeckBGY,self.deckBGWidth,self.deckBGHeight))
            self.screen.blit(self.playerDeckBG,self.playerDeckBG_Rect)
            self.screen.blit(self.player2DeckBG,self.player2DeckBG_Rect)
        else:
            pg.draw.rect(self.screen,(255,255,255),(self.player2DeckBGX,self.player2DeckBGY,self.deckBGWidth,self.deckBGHeight))
            self.screen.blit(self.playerDeckBG,self.playerDeckBG_Rect)
            self.screen.blit(self.player2DeckBG,self.player2DeckBG_Rect)
            
        
        try:
            
            self.currentPileCard = game.getCurrentPileCard()
            self.screen.blit(self.cardSprites[self.currentPileCard[CardData.Color.value]][str(self.currentPileCard[CardData.Value.value])],(300,190))
            self.drawCard = self.screen.blit(self.blankCard,(410,190))

            playerDeckSize : int = len(game.player1Deck if self.playerID == 0 else game.player2Deck)
            for i in range(playerDeckSize):

                lenghtDistance = self.playerDeckBG_Rect.y // playerDeckSize
                lengthIncrement = self.cardDeckWidth // playerDeckSize
                x = (i * lengthIncrement) + (lengthIncrement - lenghtDistance)

                playerCardColours = game.player1Deck[i][CardData.Color.value] if self.playerID == 0 else game.player2Deck[i][CardData.Color.value]
                playerCardValues = str(game.player1Deck[i][CardData.Value.value]) if self.playerID == 0 else str(game.player2Deck[i][CardData.Value.value])
                    
                self.playerDeckCards[(playerCardColours,playerCardValues)] = self.screen.blit(self.cardSprites[playerCardColours][playerCardValues],
                                (x,self.p1DeckPosY))
                    
                

            player2DeckSize : int = len(game.player1Deck if self.playerID == 1 else game.player2Deck)
            for j in range(player2DeckSize):

                lenghtDistance = self.playerDeckBG_Rect.y // player2DeckSize
                lengthIncrement = self.cardDeckWidth // player2DeckSize
                x = (j * lengthIncrement) + (lengthIncrement - lenghtDistance)

                self.screen.blit(self.blankCard,(x,self.p2DeckPosY))

            
        except:
            pass
                
       
        
        
        
        

            
