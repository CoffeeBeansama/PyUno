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

        self.uno = False

        self.startingCards = 3

        self.createCards()

        self.currentColor = None

        self.sortedData = {
            "PlayerTurn" : self.incrementTurn,
            "Draw Single Card" : self.drawSingleCard,
            "Draw Multiple Cards" : self.drawMultipleCards,
            "Plus Two" : self.addPlusTwoCardStreak,
            "Plus Four" : self.addPlusFourCardStreak,
            "Ready" : self.playerReady,
            "Game Begin" : self.roundBegin,
            "Called Uno" : self.calledUno,
            "Blue" : self.setCurrentColor,
            "Red" : self.setCurrentColor,
            "Green" : self.setCurrentColor,
            "Yellow" : self.setCurrentColor

        }

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
        
#region getters & setters
    def getCurrentTurn(self):
        return self.turn

    def getCurrentDrawStreak(self):
        return self.cardDrawStreak
    
    def gameUno(self):
        return self.uno

    def getPlayerOneData(self):
        return self.data["PlayerOne"]
    
    def getPlayerTwoData(self):
        return self.data["PlayerTwo"]
    
    def getCurrrentColor(self):
        return self.currentColor

    def getCurrentPileCard(self):
        return self.pile[-1]

    def bothPlayersReady(self):
        if self.playersReady[0] and self.playersReady[1]:
            return True
        return False
#endregion

#region Data Sorting

    def processData(self,player,data):
        processedData = self.sortedData.get(data,self.updatePlayerData)
        processedData(player,data)

    def playerReady(self,player,data):
        match player:
            case 0:
                self.playersReady[0] = True
            case 1:
                self.playersReady[1] = True

    def drawMultipleCards(self,player,data):
        for i in range(0,self.cardDrawStreak):
            if player == 0:
                self.player1Deck.append(self.cardDeck[i])
                self.cardDeck.pop(i)
            elif player == 1:
                self.player2Deck.append(self.cardDeck[i])
                self.cardDeck.pop(i)
                
        self.cardDrawStreak = 0
        self.incrementTurn(player,data)

    def setCurrentColor(self,player,data):
        self.currentColor = data

    def updatePlayerData(self,player,data):
        player1DeckSize : int = len(self.player1Deck)
        player2DeckSize : int = len(self.player2Deck)

        if player1DeckSize >= 2:
            self.uno = False
        if player2DeckSize >= 2:
            self.uno = False
        
        try:
            if player == 0:
                player1Data = ast.literal_eval(str(data))
                self.data["PlayerOne"] = player1Data["Player"]
                if player1Data["PlayerTurn"] is not None:
                    if player1Data["PlayerTurn"] in self.player1Deck:
                        self.pile.append(player1Data["PlayerTurn"])
                        self.player1Deck.remove(player1Data["PlayerTurn"])
                        self.incrementTurn(player,data)
            elif player == 1:
                player2Data = ast.literal_eval(str(data))
                self.data["PlayerTwo"] = player2Data["Player"]
                if player2Data["PlayerTurn"] is not None:
                    if player2Data["PlayerTurn"] in self.player2Deck:
                        self.pile.append(player2Data["PlayerTurn"])
                        self.player2Deck.remove(player2Data["PlayerTurn"])
                        self.incrementTurn(player,data)
        except:
            pass

    def addPlusTwoCardStreak(self,player,data):
        self.cardDrawStreak += 2
    
    def addPlusFourCardStreak(self,player,data):
        self.cardDrawStreak += 4
    
    def incrementTurn(self,player,data):
        self.turn += 1
        if self.turn >= 2:
            self.turn = 0
        
    def drawSingleCard(self,player,data):
        if player == 0:
            self.player1Deck.append(self.cardDeck[0])
            self.cardDeck.pop(0)
        elif player == 1:
            self.player2Deck.append(self.cardDeck[0])
            self.cardDeck.pop(0)
        self.incrementTurn(player,data)
    
    def roundBegin(self,player,data):
        for cards in self.cardDeck[:self.startingCards]:
            self.player1Deck.append(cards)
            self.cardDeck.remove(cards)
        for cards in self.cardDeck[:self.startingCards]:
            self.player2Deck.append(cards)
            self.cardDeck.remove(cards)
        
        for index,item in enumerate(self.cardDeck):
            if item[CardData.Value.value] not in ["Wild","WildDraw"]:
                self.pile.append(item)
                self.cardDeck.pop(index)
                return
        
        self.currentColor = self.pile[0][CardData.Color.value]
        return
    
    def roundBegin(self,player,data):
        for cards in self.cardDeck[:self.startingCards]:
            self.player1Deck.append(cards)
            self.cardDeck.remove(cards)
        for cards in self.cardDeck[:self.startingCards]:
            self.player2Deck.append(cards)
            self.cardDeck.remove(cards)
        
        for index,item in enumerate(self.cardDeck):
            if item[CardData.Value.value] not in ["Wild","WildDraw"]:
                self.pile.append(item)
                self.cardDeck.pop(index)
                return
        
        self.currentColor = self.pile[0][CardData.Color.value]
        return
    
    def calledUno(self,player,data):
        player1DeckSize : int = len(self.player1Deck)
        player2DeckSize : int = len(self.player2Deck)
        if player == 0:
            if player1DeckSize <= 1:
                self.uno = True
            if player2DeckSize == 1:
                self.drawTwoCards(self.player2Deck)
        elif player == 1:
            if player2DeckSize <= 1:
                self.uno = True
            if player1DeckSize == 1:
                self.drawTwoCards(self.player1Deck)

    def drawTwoCards(self,playerDeck):
        for i in range(0,2):
            playerDeck.append(self.cardDeck[i])
            self.cardDeck.pop(i)
        self.uno = True

#endregion