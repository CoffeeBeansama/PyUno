import sys
import pygame as pg
from network import Network
import ast
from settings import *
from sceneCache import SceneCache
from eventhandler import EventHandler

class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((width,height))
        
        self.running = True
        self.FPS = 60
        self.clock = pg.time.Clock()


        self.playerData = {
            "Player" : {},
            "PlayerTurn" : None
        }
        
        self.connectToServer()
        
        self.sceneCache = SceneCache(self)
        self.currentScene = self.sceneCache.mainMenu()

        fontPath = "Fonts/DeterminationMonoWebRegular-Z5oq.ttf"
        self.fontColor = (255,255,255)
        self.fpsFont = pg.font.Font(fontPath,18)
        
        pg.display.set_caption("PyUno")
    
    def connectToServer(self):
        self.network = Network()
        try:
            self.playerID = int(self.network.getPlayerID())
        except:
            pass

    def displayFPS(self):
         fps = self.fpsFont.render(f"{round(self.clock.get_fps())}",True,self.fontColor)
         pos = (670,10)
         self.window.blit(fps,pos)

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.network.disconnectPlayer()
                    self.running = False
                    pg.quit()
                    sys.exit()

            self.window.fill("black")
            EventHandler.handleKeyBoardInput() 

            try:
                self.game = self.network.send("get")
                self.currentScene.update(self.game)
            except:
                pass
            
            self.displayFPS()
            pg.display.update()
            self.clock.tick(self.FPS)



if __name__ == "__main__":
    game = Game()
    game.run()
