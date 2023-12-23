import pygame as pg
from support import loadSprite,import_folder
from settings import PlayerData
from eventhandler import EventHandler

class Player(pg.sprite.Sprite):
    def __init__(self,id,pos,groups,collisionSprites,interactables):
        super().__init__(groups)

        self.id = id
        self.collisionSprites = collisionSprites
        self.interactableSprites = interactables

        self.importSprites()
        self.image = pg.image.load(f"{self.spritePath}Idle_Down/180.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)

        self.walkingAnimationTime = 1 / 8
        self.speed = 1
        self.frame_index = 0

        self.state = "Idle_Down"
        self.direction = pg.math.Vector2()

        self.data = {}

    def importSprites(self):
        self.animationStates = {
            "Up": [], "Down": [], "Left": [], "Right" : [],
            "Idle_Down": [],"Idle_Up": [], "Idle_Left": [] , "Idle_Right": [],
            
        }

        self.spritePath = f"Sprites/Player{1}/" if self.id == 0 else f"Sprites/Player{2}/"

        for animations in self.animationStates.keys():
            fullPath = self.spritePath + animations
            self.animationStates[animations] = import_folder(fullPath)

    def handleObjectInteraction(self):
        for objects in self.interactableSprites:
            if hasattr(objects,"interactHitbox"):
                if objects.interactHitbox.colliderect(self.hitbox):
                    objects.interact()
                else:
                    objects.ignore()

    def handleMovement(self):
        self.hitbox.x += self.direction.x * self.speed
        self.handleWallCollision("Horizontal")
        self.hitbox.y += self.direction.y * self.speed
        self.handleWallCollision("Vertical")
        self.rect.center = self.hitbox.center

    def handleAnimation(self):
        animation = self.animationStates[self.state]
        self.frame_index += self.walkingAnimationTime 

        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        

    def idleState(self):
        self.direction.x = 0 
        self.direction.y = 0
        
        if not "Idle" in self.state:
            self.state = f"Idle_{self.state}"
    
    def handleVerticalMovement(self,value,state):
        self.direction.x = 0
        self.direction.y = value
        self.state = state

    def handleHorizontalMovement(self,value,state):
        self.direction.x = value
        self.direction.y = 0
        self.state = state

    def handleWallCollision(self, direction):
        for sprite in self.collisionSprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == "Horizontal":
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    else:
                        self.hitbox.right = sprite.hitbox.left
                elif direction == "Vertical":
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    else:
                        self.hitbox.bottom = sprite.hitbox.top

    def handleInputs(self):
        if EventHandler.pressingUpKey():
            self.handleVerticalMovement(-1,"Up")
        elif EventHandler.pressingDownKey():
            self.handleVerticalMovement(1,"Down")
        elif EventHandler.pressingLeftKey():
            self.handleHorizontalMovement(-1,"Left")
        elif EventHandler.pressingRightKey():
            self.handleHorizontalMovement(1,"Right")
        else:
            self.idleState()

    def handlePlayer2Movement(self,pos,frameIndex,state):
        self.hitbox.center = pos
        self.rect.center = pos
        self.state = state
        self.frame_index = frameIndex
        self.image : pg.Surface = self.animationStates[self.state][int(self.frame_index)]

    def update(self):
        self.data[PlayerData.Position.value] = self.rect.center
        self.data[PlayerData.State.value] = self.state
        self.data[PlayerData.FrameIndex.value] = self.frame_index

        self.handleInputs()
        self.handleAnimation()
        self.handleMovement()
        self.handleObjectInteraction()
        
        
        
