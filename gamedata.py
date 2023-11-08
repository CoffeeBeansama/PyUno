import pygame as pg
import random
import ast
from settings import CardData

class Card:
    def __init__(self,value,color=None):
        
        self.value = value
        self.color = color

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

        self.createCards()


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
        return

    def incrementTurn(self):
        self.turn += 1
        if self.turn >= 2:
            self.turn = 0
        

    def getCurrentTurn(self):
        return self.turn

    def updatePlayerOneData(self,data):
        try:
            player1Data = ast.literal_eval(str(data))
            self.data["PlayerOne"] = player1Data["Player"]
            
            if player1Data["PlayerTurn"] is not None:
                if player1Data["PlayerTurn"] in self.player1Deck:
                    print(player1Data["PlayerTurn"])
                    self.player1Deck.remove(player1Data["PlayerTurn"])
                
        except:
            pass
        
    def updatePlayerTwoData(self,data):
        try:
            player2Data = ast.literal_eval(str(data))
            self.data["PlayerTwo"] = player2Data["Player"]
            
            if player2Data["PlayerTurn"] is not None:
                if player2Data["PlayerTurn"] in self.player2Deck:
                    print(player2Data["PlayerTurn"])
                    self.player2Deck.remove(player2Data["PlayerTurn"])
            
        except:
            pass

    def getPlayerOneData(self):
        return self.data["PlayerOne"]
    
    def getPlayerTwoData(self):
        return self.data["PlayerTwo"]
    
    def playerReady(self,player):
        match player:
            case 0:
                self.playersReady[0] = True
            case 1:
                self.playersReady[1] = True

    

    def bothPlayersReady(self):
        if self.playersReady[0] and self.playersReady[1]:
            return True
        
        return False