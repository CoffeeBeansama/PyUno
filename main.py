import pygame as pg
from network import Network
import ast
from player import Player
from camera import CameraGroup

class Game:
    def __init__(self):
        self.window = pg.display.set_mode((700,500))
    
        self.running = True
        self.FPS = 60
        self.clock = pg.time.Clock()

        
        self.network = Network()
        self.visibleSprites = CameraGroup()

        try:
            self.playerID = int(self.network.getPlayerID())
        except:
            pass
        
        p1Pos = (100,100)
        p2Pos = (150,100)
        self.player = Player(self.playerID,p1Pos if self.playerID == 0  else p2Pos,self.visibleSprites)
        self.player2 = Player(self.playerID+1 if self.playerID == 0 else 0,p2Pos if self.playerID == 0 else p1Pos,self.visibleSprites)

        self.gameData = {
            "Player" : {}
        }

        pg.display.set_caption(f"Player {str(self.playerID+1)}")

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()

            self.window.fill("black")
            
            self.game = self.network.send("get")

            self.player.update()
            self.gameData["Player"] = self.player.data
            
            self.network.send(str(self.gameData))

            
            match self.playerID:
                case 0:
                    if type(self.game.getPlayerTwoData()) == str:
                        
                        data = ast.literal_eval(str(self.game.getPlayerTwoData()))
                        playerData = data["Player"]
                        
                        self.player2.handlePlayer2Movement(playerData["Pos"],playerData["FrameIndex"],playerData["State"])
                case 1:
                    if type(self.game.getPlayerOneData()) == str:
                        
                        data = ast.literal_eval(str(self.game.getPlayerOneData()))
                        playerData = data["Player"]
                        
                        self.player2.handlePlayer2Movement(playerData["Pos"],playerData["FrameIndex"],playerData["State"])
                        
            

            self.visibleSprites.custom_draw(self.player)
            pg.display.update()
            self.clock.tick(self.FPS)

game = Game()
game.run()