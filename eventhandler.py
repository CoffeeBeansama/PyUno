import pygame as pg

class EventHandler(object):
    
    pressingUp = False
    pressingDown = False
    pressingRight = False
    pressingLeft = False

    @staticmethod
    def handleKeyBoardInput():
        keys = pg.key.get_pressed()

        EventHandler.pressingUp = True if keys[pg.K_UP] else False
        EventHandler.pressingDown = True if keys[pg.K_DOWN] else False
        EventHandler.pressingLeft = True if keys[pg.K_LEFT] else False
        EventHandler.pressingRight = True if keys[pg.K_RIGHT] else False

    def pressingUpKey():
        return EventHandler.pressingUp

    def pressingDownKey():
        return EventHandler.pressingDown

    def pressingLeftKey():
        return EventHandler.pressingLeft

    def pressingRightKey():
        return EventHandler.pressingRight
