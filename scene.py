import pygame as pg
from abc import ABC,abstractmethod

class Scene(ABC):
    def __init__(self,sceneCache,game):
        self.screen = pg.display.get_surface()
        self.sceneCache = sceneCache
        self.game = game

    @abstractmethod
    def update(self):
        pass

    def switchScene(self,newScene):
        self.game.currentScene = newScene