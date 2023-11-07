from enum import Enum

width,height = 700,500
port = 5558

class PlayerData(Enum):
    Position = 1
    State = 2
    FrameIndex = 3

class MapTiles(Enum):
    Walls = 1
    InteractableObjects = 2


