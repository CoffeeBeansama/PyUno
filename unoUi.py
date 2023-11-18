import pygame as pg
from support import loadSprite
from timer import Timer

class UnoUi:
    def __init__(self,playerUNO):
        self.screen = pg.display.get_surface()
        self.timer = Timer(300)
        self.unoSprite = loadSprite("Sprites/Uno.png",(150,90)).convert_alpha()
        self.unoSpriteRect = self.unoSprite.get_rect(topleft=(540,200))
        self.unoUi = self.screen.blit(self.unoSprite,self.unoSpriteRect)
        self.playerUNO = playerUNO

    def renderUno(self):
        self.timer.update()
        mousePos = pg.mouse.get_pos()
        mousePressed = pg.mouse.get_pressed()

        self.unoUi = self.screen.blit(self.unoSprite,self.unoSpriteRect)
        
        if self.unoUi.collidepoint(mousePos):
            if mousePressed[0]:
                if not self.timer.activated:
                    self.playerUNO()
                    self.timer.activate()