import pygame, math

from gameScripts import entities

class InteractiveObject:
    def __init__(self, position, radius: int, possibleActions : list) -> None:
        self.possibleActions = possibleActions
        self.position = position
        self.radius : int = radius
        self.rect = pygame.Rect(position[0] - (self.radius * 1.2), position[1] - self.radius, self.radius, self.radius)
        self.interactable : bool = False

        self.button = pygame.image.load(".venv/images/interactButton.png")

    def checkCollision(self, player : entities.Player, surface : pygame.Surface, coords):
        if self.rect.colliderect(player.rect()):
            self.interactable = True
            surface.blit(self.button, [coords[0] + 4, coords[1] - 20])
        else:
            self.interactable = False

    def interact(self, surface : pygame.Surface, action : str = "dialogue"):
        if action in self.possibleActions:
            print("Player interagiu com o objeto")