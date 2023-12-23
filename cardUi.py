import pygame as pg
from support import loadSprite
from settings import *
from timer import Timer

class CardUi:
    def __init__(self,playerID,playerTurn,drawSingleCard):
        self.screen = pg.display.get_surface()
        self.playerID = playerID
        self.playerTurn = playerTurn
        self.drawSingleCard = drawSingleCard
    
        self.initializeFont()
       
        self.importCardSprites()
        
        self.renderColours = False

        self.initializePlayerDeck()
        self.initializePlayerTwoDeck()

        self.deletedCard = None
        
        self.timer = Timer(300)

    
    def initializeFont(self):
        pg.font.init()
        self.fontColor = (255,255,255)
        fontPath = "Fonts/DeterminationMonoWebRegular-Z5oq.ttf"
        self.gameFont = pg.font.Font(fontPath,64)
   
    def initializePlayerDeck(self): 
        self.playerDeckCards = {}

        self.playerDeckBG = loadSprite("Sprites/playerDeckBg.png",(660,150))
        self.playerDeckBG_Rect = self.playerDeckBG.get_rect(topleft=(20,340))
        self.playerDeckBG.set_alpha(240)

        self.playerDeckBGX = 15
        self.playerDeckBGY = 335

        self.deckBGWidth = 670
        self.deckBGHeight = 160
       
        self.cardDeckWidth = 625
        self.p1DeckPosY = 355
    
    def initializePlayerTwoDeck(self): 
        self.player2DeckBGX = 15
        self.player2DeckBGY = 5

        self.player2DeckBG = self.playerDeckBG
        self.player2DeckBG_Rect = self.player2DeckBG.get_rect(topleft=(20,10))
        
        self.p2DeckPosY = 20

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

        self.colorCards = ["0","1","2","3","4","5","6","7","8","9","Draw","Reverse","Skip"]
        self.cardSize = (80,120)
        self.blankCard = loadSprite("Sprites/Uno Game Assets/Deck.png",self.cardSize).convert_alpha()
        self.drawCard = self.screen.blit(self.blankCard,(410,190))
        self.wildCards = ["Wild","WildDraw"]

        self.getColorCards("Blue")
        self.getColorCards("Red")
        self.getColorCards("Yellow")
        self.getColorCards("Green")
        self.getWildCards("WildCards")


    def getColorCards(self,color):
        for sprites in self.colorCards:
            self.cardSprites[color][sprites] = loadSprite(f"{self.cardSpritePath}{color}/{color}_{sprites}.png",self.cardSize).convert_alpha()
            
    def getWildCards(self,color):
        for sprites in self.wildCards:
            self.cardSprites[color][sprites] = loadSprite(f"{self.cardSpritePath}{color}/{sprites}.png",self.cardSize).convert_alpha()
        


    def displayCards(self):
        self.screen.blit(self.blankCard,(100,100))
       
    def renderPlayerWon(self,win):
        if win:
            pos = (230,375)
            status = self.gameFont.render("You Win!",True,self.fontColor)
        else:
            pos = (160,45)
            status = self.gameFont.render("Player 2 Win!",True,self.fontColor)
        
        self.screen.blit(status,pos)

    def cardSelection(self,mousePos,mousePressed):
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

    def drawFromPile(self,mousePos,mousePressed):
        if self.drawCard.collidepoint(mousePos):
            if mousePressed[0]:
                if not self.timer.activated:
                    self.drawSingleCard()
                    self.timer.activate()

    def handleUiEvent(self):
        self.timer.update()
        self.cardSelection(self.mousePos,self.mousePressed)
        self.drawFromPile(self.mousePos,self.mousePressed)
    
    def highlightPlayerTurnDeck(self,turn,playerID):
        white = (255,255,255)
        if turn == playerID:
            pg.draw.rect(self.screen,white,(self.playerDeckBGX,self.playerDeckBGY,self.deckBGWidth,self.deckBGHeight))
        else:
             pg.draw.rect(self.screen,white,(self.player2DeckBGX,self.player2DeckBGY,self.deckBGWidth,self.deckBGHeight))


    def renderPlayerDeck(self,game):
        self.currentPileCard = game.getCurrentPileCard()
        self.screen.blit(self.cardSprites[self.currentPileCard[CardData.Color.value]][str(self.currentPileCard[CardData.Value.value])],(300,190))
        playerDeckSize : int = len(game.player1Deck if self.playerID == 0 else game.player2Deck)
        for i in range(playerDeckSize):

            lenghtDistance = self.playerDeckBG_Rect.y // playerDeckSize
            lengthIncrement = self.cardDeckWidth // playerDeckSize
            x = (i * lengthIncrement) + (lengthIncrement - lenghtDistance)

            playerCardColours = game.player1Deck[i][CardData.Color.value] if self.playerID == 0 else game.player2Deck[i][CardData.Color.value]
            playerCardValues = str(game.player1Deck[i][CardData.Value.value]) if self.playerID == 0 else str(game.player2Deck[i][CardData.Value.value])
                    
            self.playerDeckCards[(playerCardColours,playerCardValues)] = self.screen.blit(self.cardSprites[playerCardColours][playerCardValues],
                            (x,self.p1DeckPosY))


    def renderPlayer2Deck(self,game):
        player2DeckSize : int = len(game.player1Deck if self.playerID == 1 else game.player2Deck)
        for j in range(player2DeckSize):
            lenghtDistance = self.playerDeckBG_Rect.y // player2DeckSize
            lengthIncrement = self.cardDeckWidth // player2DeckSize
            x = (j * lengthIncrement) + (lengthIncrement - lenghtDistance)

            self.screen.blit(self.blankCard,(x,self.p2DeckPosY))

    def handleRendering(self,game,turn,playerID):
        self.timer.update()
        self.mousePos = pg.mouse.get_pos()
        self.mousePressed = pg.mouse.get_pressed()

    
        self.highlightPlayerTurnDeck(turn,playerID)
        self.screen.blit(self.playerDeckBG,self.playerDeckBG_Rect)
        self.screen.blit(self.player2DeckBG,self.player2DeckBG_Rect) 

        self.drawCard = self.screen.blit(self.blankCard,(410,190))

        try:        
            self.renderPlayerDeck(game)
            self.renderPlayer2Deck(game)
        except:
            pass
                
    
    def update(self,game,turn,playerID):
        
        self.handleRendering(game,turn,playerID)
        self.handleUiEvent()
        
        
        
        

            
