import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image = pg.transform.scale(pg.image.load("Sprites/player.png"),(16,16))

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)










