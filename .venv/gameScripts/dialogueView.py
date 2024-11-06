import pygame
import time
import pygame.freetype
import pygame_gui

import json
# classe pra lidar com diálogos
# ainda falta pensar em como isso funcionaria
class DialogueView:
    def __init__(self, npc, lines : str = '', dialogueBoxSprite = None) -> None:
        if '\n' in lines:
            self.lines = lines.split("\n")
        else:
            self.lines = lines
        self.npc = npc
        self.textFont = pygame.freetype.SysFont("Monocraft", 24)

        if type(self.lines) == list:
            self.textRect = self.textFont.get_rect(self.lines[0])
        else:
            self.textRect = self.textFont.get_rect(self.lines)

        self.drawable : bool = False

        self.dialogueFile = ''

        self.currentLine : str = '1'

    def draw(self, surface : pygame.Surface, player, uiManager):
        if self.lines != "":
            player.movable = False
            with open('.venv/dialogues/debugDialogue.json', 'r') as file:
                btnsQtd = len(json.load(file)['debugCat'][self.currentLine]) - 1
            self.textFont.render_to(surface, self.textRect.topleft, self.lines, (255, 255, 255), (231, 15, 150))

            for i in range(btnsQtd):
                pygame_gui.elements.UIButton(pygame.Rect(150, 200 + 55*i, 100, 50), 'debug', uiManager)
        # surface.blit(img, surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2)))