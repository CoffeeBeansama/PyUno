import pygame as pg
from abc import ABC,abstractmethod

class Scene(ABC):
    def __init__(self,sceneCache,game):
        pg.font.init()
        self.screen = pg.display.get_surface()
        self.sceneCache = sceneCache
        self.game = game
        self.fontPath = "Fonts/DeterminationMonoWebRegular-Z5oq.ttf"

    @abstractmethod
    def update(self):
        pass

    def switchScene(self,newScene):
        self.game.currentScene = newScene