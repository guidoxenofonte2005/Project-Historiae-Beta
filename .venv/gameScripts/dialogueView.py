import pygame
# classe pra lidar com diálogos
# ainda falta pensar em como isso funcionaria
class DialogueView:
    def __init__(self, lines : str, npc, dialogueBoxSprite = None) -> None:
        self.lines = lines.splitlines()
        self.npc = npc
        self.textFont = pygame.font.SysFont("smwwholepixelspacingregular", 20)

    def printText(self, text : str):
        img = self.textFont.render(text, True, (0,0,0))
    
    def update(self, surface : pygame.Surface):
        for line in self.lines:
            self.printText(line)

    def breakDown(self):
        pass