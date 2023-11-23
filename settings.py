from enum import Enum

width,height = 700,500
port = 5559


class CardData(Enum):
    Value = 0
    Color = 1    

class PlayerData(Enum):
    Position = 1
    State = 2
    FrameIndex = 3

class MapTiles(Enum):
    Walls = 1
    InteractableObjects = 2


