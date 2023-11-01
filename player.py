import pygame as pg
from pygame.sprite import _Group
from support import loadSprite


class Player(pg.sprite.Sprite):
    def __init__(self,id,pos,groups):
        super().__init__(groups)

        self.id = id
        self.spritePath = "Sprites/Player1/" if self.id == 0 else "Sprites/Player2"

        self.image = pg.image.load(f"{self.spritePath}Idle_Down/180.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)

        self.speed = 1

    def update(self):
        pass