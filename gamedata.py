import pygame as pg
import random
import ast
from settings import CardData

class Game:
    def __init__(self,id):
        self.id = id
        
        self.playersReady = [False,False]

        self.data = {
            "PlayerOne" : None,
            "PlayerTwo" : None
        }
        

        self.pile = []
        self.player1Deck = []
        self.player2Deck = []
        self.cardDeck = []

        self.powerCards = ["Draw","Reverse","Skip"]
        self.wildCards = ["Wild", "WildDraw"]
        self.numberCards = [i for i in range(0,10)]

        self.turn = 0
        self.cardDrawStreak = 0

        

        self.createCards()

        self.currentColor = None


    def createColorCards(self,color):
        for i in range(2):
            for j in range(len(self.numberCards)):
                self.cardDeck.append((str(self.numberCards[j]),color))

            for k in range(len(self.powerCards)):
                self.cardDeck.append((str(self.powerCards[k]),color))

    def createWildCards(self):
        for i in range(4):
            for j in range(len(self.wildCards)):
                self.cardDeck.append((self.wildCards[j],"WildCards"))
    
    def createCards(self):
        self.createColorCards("Blue")
        self.createColorCards("Green")
        self.createColorCards("Red")
        self.createColorCards("Yellow")

        self.createWildCards()

        random.shuffle(self.cardDeck)
        
    
    def roundBegin(self):
        for cards in self.cardDeck[:7]:
            self.player1Deck.append(cards)
            self.cardDeck.remove(cards)
        for cards in self.cardDeck[:7]:
            self.player2Deck.append(cards)
            self.cardDeck.remove(cards)
        
        for index,item in enumerate(self.cardDeck):
            if item[CardData.Value.value] not in ["Wild","WildDraw"]:
                self.pile.append(item)
                self.cardDeck.pop(index)
                return
        
        self.currentColor = self.pile[0][CardData.Color.value]
       
        return
    
    

    def incrementTurn(self):
        self.turn += 1
        if self.turn >= 2:
            self.turn = 0
        
    def drawSingleCard(self,player):
        if player == 0:
            self.player1Deck.append(self.cardDeck[0])
            self.cardDeck.pop(0)
        elif player == 1:
            self.player2Deck.append(self.cardDeck[0])
            self.cardDeck.pop(0)
        self.incrementTurn()

    def getCurrentTurn(self):
        return self.turn

    def getCurrentDrawStreak(self):
        return self.cardDrawStreak
    
    def addPlusTwoCardStreak(self):
        self.cardDrawStreak += 2
    
    def addPlusFourCardStreak(self):
        self.cardDrawStreak += 4

    def updatePlayerData(self,player,data):
        try:
            if player == 0:
                player1Data = ast.literal_eval(str(data))
                self.data["PlayerOne"] = player1Data["Player"]
                if player1Data["PlayerTurn"] is not None:
                    if player1Data["PlayerTurn"] in self.player1Deck:
                        self.pile.append(player1Data["PlayerTurn"])
                        self.player1Deck.remove(player1Data["PlayerTurn"])
                        self.incrementTurn()
            elif player == 1:
                player2Data = ast.literal_eval(str(data))
                self.data["PlayerTwo"] = player2Data["Player"]
                if player2Data["PlayerTurn"] is not None:
                    if player2Data["PlayerTurn"] in self.player2Deck:
                        self.pile.append(player2Data["PlayerTurn"])
                        self.player2Deck.remove(player2Data["PlayerTurn"])
                        self.incrementTurn()
        except:
            pass
    
    def playerUno(self):
        pass

    def getPlayerOneData(self):
        return self.data["PlayerOne"]
    
    def getPlayerTwoData(self):
        return self.data["PlayerTwo"]
    
    def drawMultipleCards(self,player):
        for i in range(0,self.cardDrawStreak):
            if player == 0:
                self.player1Deck.append(self.cardDeck[i])
                self.cardDeck.pop(i)
            elif player == 1:
                self.player2Deck.append(self.cardDeck[i])
                self.cardDeck.pop(i)
                
        self.cardDrawStreak = 0
        self.incrementTurn()

    def playerReady(self,player):
        match player:
            case 0:
                self.playersReady[0] = True
            case 1:
                self.playersReady[1] = True

    def setCurrentColor(self,color):
        self.currentColor = color
        

    def getCurrrentColor(self):
        return self.currentColor

    def getCurrentPileCard(self):
        return self.pile[-1]

    def bothPlayersReady(self):
        if self.playersReady[0] and self.playersReady[1]:
            return True
        
        return False