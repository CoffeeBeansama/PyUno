from enum import Enum

class PlayerData(Enum):
    Position = 1
    State = 2
    FrameIndex = 3

class MapTiles(Enum):
    Walls = 1
    InteractableObjects = 2

colorCards = ["0","1","2","3","4","5","6","7","8","9","Draw","Reverse","Skip"]
wildCards = ["Wild","WildDraw"]