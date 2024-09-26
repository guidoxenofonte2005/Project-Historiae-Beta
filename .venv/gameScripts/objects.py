import pygame, math

from gameScripts import entities

class InteractiveObject:
    def __init__(self, position, radius: int) -> None:
        self.position = position
        self.radius : int = radius
        self.rect = pygame.Rect(position[0] - self.radius, position[1] - self.radius, self.radius, self.radius)
        self.interactable : bool = False

        self.button = pygame.image.load(".venv/images/interactButton.png")

    def checkCollision(self, player : entities.Player):
        if self.rect.colliderect(player.rect()):
            self.interactable = True
        else:
            self.interactable = False

    def interact(self, surface : pygame.Surface, coords):
        if self.interactable:
            surface.blit()