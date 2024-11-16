import pygame, math
import json

from gameScripts import entities
from gameScripts.dialogueView import DialogueView

class InteractiveObject:
    def __init__(self, position, radius: int, possibleActions : list[str], game, name : str = "debugCat") -> None:
        self.name = name
        self.possibleActions = possibleActions
        self.position = position
        self.radius : int = radius
        self.rect = pygame.Rect(position[0] - (self.radius * 1.2), position[1] - self.radius, self.radius, self.radius)
        self.interactable : bool = False

        self.button = pygame.image.load(".venv/images/interactButton.png")

        self.animation = game.assets[name].copy()

    def checkCollision(self, player : entities.Player, surface : pygame.Surface, coords):
        if self.rect.colliderect(player.rect()):
            self.interactable = True
            surface.blit(self.button, [coords[0] + 4, coords[1] - 20])
        else:
            self.interactable = False
        return self.interactable

    def interact(self, surface : pygame.Surface, offset : tuple, dialogueView : DialogueView, phase : str, action : str = "dialogue", dialogueFile : str = ".venv/dialogues/debugDialogue.txt"):
        if self.interactable:
            if action in self.possibleActions:
                self.interactable = False
                if action == "dialogue":
                    with open(".venv/dialogues/debugDialogue.json", 'r') as file:
                        tempLines = json.load(file)
                    dialogueView.lines = tempLines[self.name]['1']["Dialogue"]
                    dialogueView.dialogueFile = dialogueFile
                elif action == "changeArea":
                    return "changeArea"
                else:
                    print("\033[31mInvalid action\033[m")
            return 'interacting'
        return 'normal'
    
    def render(self, surface : pygame.Surface, offset : tuple):
        surface.blit(pygame.transform.flip(self.animation.image(), False, False), (self.position[0] - offset[0] - self.radius, self.position[1] - offset[1] - self.radius))
