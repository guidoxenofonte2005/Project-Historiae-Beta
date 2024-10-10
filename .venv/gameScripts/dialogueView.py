import pygame
import time
# classe pra lidar com diálogos
# ainda falta pensar em como isso funcionaria
class DialogueView:
    def __init__(self, lines : str, npc, dialogueBoxSprite = None) -> None:
        self.lines = lines.split("\n")
        self.npc = npc
        self.textFont = pygame.font.SysFont("Arial", 20)

    def printText(self, text : str, surface : pygame.Surface, charOffset : tuple):
        # counter : int = 0
        # speed : int = 3
        # text = "Check this out"
        # while (counter <= speed * len(text)):
        #     img = self.textFont.render(str(text[0:counter//speed]), True, (0,0,0))
        #     surface.blit(img, (charOffset[0], charOffset[1]))
        #     counter += 1
        #     pygame.display.update()
        pass
    
    def update(self, surface : pygame.Surface, offset : tuple):
        # for line in self.lines:
        #     self.printText(line, surface, offset)
        print("Player interagiu com esse objeto")