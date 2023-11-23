import pygame as pg
from scene import Scene

class MainMenu(Scene):
    def __init__(self,stateCache,game):
        super().__init__(stateCache,game)
        

        self.black = (0,0,0)
        self.white = (255,255,255)

        self.fontColor = self.white
        
        self.titleFont = pg.font.Font(self.fontPath,88)
        self.buttonFont = pg.font.Font(self.fontPath,36)
        self.gameStart = False

        self.buttonTextColor = self.white
        self.buttonColor = self.black
        width = 150
        height = 40
        self.startButton = pg.draw.rect(self.screen,self.buttonColor,(275,220,width,height))

    def handleEvent(self):
        mousePos = pg.mouse.get_pos()
        mousePressed = pg.mouse.get_pressed()

        if self.startButton.collidepoint(mousePos):
            self.buttonColor = self.white
            self.buttonTextColor = self.black
            if mousePressed[0]:
                self.switchScene(self.sceneCache.overWorld())
        else:
            self.buttonColor = self.black
            self.buttonTextColor = self.white

    def update(self,gameData=None):
        title = self.titleFont.render("PyUno",True,self.fontColor)
        titlePos = (245,60)

        self.handleEvent()
        self.screen.blit(title,titlePos)

        width = 150
        height = 40
        self.startButton = pg.draw.rect(self.screen,self.buttonColor,(275,220,width,height))


        buttonText = self.buttonFont.render("Start",True,self.buttonTextColor)
        buttonTextPos = (305,220)
        self.screen.blit(buttonText,buttonTextPos)
