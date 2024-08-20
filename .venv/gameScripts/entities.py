import pygame

class PhysicsEntity:
    def __init__(self, game, entityType, position, size) -> None:
        self.game = game
        self.type = entityType
        self.position = list(position)
        self.size = size

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    
    def update(self, tilemap, movement = (0, 0)):
        pass

class NPC(PhysicsEntity):
    pass

class Player(PhysicsEntity):
    pass