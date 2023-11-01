import pygame as pg
from network import Network
import ast


class Game:
    def __init__(self):
        self.window = pg.display.set_mode((700,500))
    
        self.running = True
        self.FPS = 60
        self.clock = pg.time.Clock()

        self.network = Network()
        try:
            self.playerID = int(self.network.getPlayerID())
        except:
            pass

        

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()

            self.window.fill("black")
            
            self.game = self.network.send("get")

            pg.display.update()
            self.clock.tick(self.FPS)

game = Game()
game.run()