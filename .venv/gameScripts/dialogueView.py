import pygame
import time
import pygame_gui
# classe pra lidar com diálogos
# ainda falta pensar em como isso funcionaria
class DialogueView:
    def __init__(self, npc, lines : str = '', dialogueBoxSprite = None) -> None:
        if '\n' in lines:
            self.lines = lines.split("\n")
        else:
            self.lines = lines
        self.npc = npc
        self.textFont = pygame.font.SysFont("Arial", 20)

        self.drawable : bool = False

    def printText(self, text : str, surface : pygame.Surface, charOffset : tuple):
        counter : int = 0
        speed : int = 3
        text = "Check this out"
        while (counter <= speed * len(text)):
            img = self.textFont.render(str(text[0:counter//speed]), True, (0,0,0))
            surface.blit(img, (charOffset[0], charOffset[1]))
            counter += 1
            pygame.display.update()
        pass
    
    def update(self, surface : pygame.Surface, offset : tuple):
        for line in self.lines:
            self.printText(line, surface, offset)
        print("Player interagiu com esse objeto")

    def draw(self, surface : pygame.Surface):
        img = self.textFont.render(self.lines, True, (0,0,0))
        surface.blit(img, surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2)))