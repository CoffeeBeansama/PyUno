import pygame as pg
from timer import Timer

class ColorUi:
    def __init__(self,setColor):
        self.screen = pg.display.get_surface()
        self.renderColours = False

        self.blue = None
        self.green = None
        self.red = None
        self.yellow = None

        self.colorSize = 150
        self.timer = Timer(300)

        self.setColor = setColor


    def handleUiEvent(self):
        if self.renderColours:
            self.timer.update()
            mousePos = pg.mouse.get_pos()
            mousePressed = pg.mouse.get_pressed()

            self.handleColourClickEvent(self.blue,mousePos,mousePressed,"Blue")
            self.handleColourClickEvent(self.green,mousePos,mousePressed,"Green")
            self.handleColourClickEvent(self.yellow,mousePos,mousePressed,"Yellow")
            self.handleColourClickEvent(self.red,mousePos,mousePressed,"Red")

    def handleColourClickEvent(self,ui,mousePos,mousePressed,color):
        if ui is not None:
            if ui.collidepoint(mousePos):
                if not self.timer.activated:
                    if mousePressed[0]:
                        self.setColor(color)
                        self.renderColours = False
                        self.timer.activate()


    def drawColours(self):
        if self.renderColours:
                 
            red = (255,0,0)
            self.red = pg.draw.rect(self.screen,red,(195,180,self.colorSize,self.colorSize))
            
            green = (0,255,0)
            self.green = pg.draw.rect(self.screen,green,(355,180,self.colorSize,self.colorSize))

            blue = (0,0,255)
            self.blue = pg.draw.rect(self.screen,blue,(35,180,self.colorSize,self.colorSize))

            yellow = (255, 255, 0)
            self.yellow = pg.draw.rect(self.screen,yellow,(515,180,self.colorSize,self.colorSize))

    def update(self):
        self.drawColours()
        self.handleUiEvent()