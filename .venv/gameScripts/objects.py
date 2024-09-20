import pygame, math

from gameScripts import entities

class InteractiveObject:
    def __init__(self, position) -> None:
        self.position = position
        self.radius : int = 35
        self.rect = pygame.Rect(position[0] - self.radius, position[1] - self.radius, self.radius, self.radius)
        self.interactable : bool = False

    def checkCollision(self, player : entities.Player):
        if self.rect.colliderect(player.rect()):
            self.interactable = True
        else:
            self.interactable = False

    def interact():
        pass