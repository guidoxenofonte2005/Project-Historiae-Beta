import pygame, math

from gameScripts import entities
from gameScripts.dialogueView import DialogueView

class InteractiveObject:
    def __init__(self, position, radius: int, possibleActions : list[str]) -> None:
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

    def interact(self, surface : pygame.Surface, offset : tuple, dialogueView : DialogueView, action : str = "dialogue", dialogueFile : str = ".venv/dialogues/debugDialogue.txt"):
        if self.interactable:
            if action in self.possibleActions:
                if action == "dialogue":
                    file = open(dialogueFile, "r")
                    dialogueView.lines = file.read()
                    dialogueView.update(surface, offset)
                    file.close()
                elif action == "get":
                    pass
                else:
                    print("\033[31mInvalid action\033[m")