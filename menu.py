import pygame as pg

class MainMenu:
    def __init__(self):
        pg.font.init()
        self.screen = pg.display.get_surface()

        self.black = (0,0,0)
        self.white = (255,255,255)

        self.fontColor = self.white
        fontPath = "Fonts/DeterminationMonoWebRegular-Z5oq.ttf"
        self.titleFont = pg.font.Font(fontPath,88)
        self.buttonFont = pg.font.Font(fontPath,36)
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
                self.gameStart = True
        else:
            self.buttonColor = self.black
            self.buttonTextColor = self.white

    def update(self):
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
