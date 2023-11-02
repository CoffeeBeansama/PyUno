import pygame as pg
from abc import abstractmethod

class InteractableObjects(pg.sprite.Sprite):

    @abstractmethod
    def interact(self):
        pass

    @abstractmethod
    def ignore(self):
        pass


class Chair(InteractableObjects):
    def __init__(self,pos,groups,playerIn):
        super().__init__(groups)
        
        self.image = pg.image.load("Sprites/player.png")
        self.rect = self.image.get_rect(topleft=pos)
        
        self.interactHitbox = self.rect.inflate(0,0)
        self.interacted = False

        self.playerIn = playerIn
    
    def interact(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_x]:
            if not self.interacted:
                self.playerIn()
                self.interacted = True
    
    def ignore(self):
        self.interacted = False