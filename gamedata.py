import pygame as pg
import random

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

        self.powerCards = ["+2","Reverse","Skip"]
        self.wildCards = ["Change Color", "+4"]
        self.numberCards = [i for i in range(0,10)]

        
        self.createCards()


    def createColorCards(self,color):
        for i in range(2):
            for j in range(len(self.numberCards)):
                self.cardDeck.append(Card(self.numberCards[j],color))

            for k in range(len(self.powerCards)):
                self.cardDeck.append(Card(self.powerCards[k],color))

    def createWildCards(self):
        for i in range(4):
            for j in range(len(self.wildCards)):
                self.cardDeck.append(Card(self.wildCards[j]))


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
        self.pile.append(self.cardDeck[0])
        self.cardDeck.pop(0)
        return

        
        
  
    def updatePlayerOneData(self,data):
        self.data["PlayerOne"] = data
        
    def updatePlayerTwoData(self,data):
        self.data["PlayerTwo"] = data

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