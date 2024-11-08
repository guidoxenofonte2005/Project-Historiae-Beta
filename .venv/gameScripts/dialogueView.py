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

        self.currentLine : int = 1
        self.variant : int = None

    def draw(self, surface : pygame.Surface, player, uiManager, displayedButtons : dict):
        if self.lines != "":
            player.movable = False
            with open('.venv/dialogues/debugDialogue.json', 'r') as file:
                tempArq = json.load(file)
                if len(tempArq['debugCat']) == 1 or self.currentLine == 1:
                    btnsQtd = len(tempArq['debugCat'][str(self.currentLine)]) - 1
                else:
                    btnsQtd = len(tempArq['debugCat'][str(self.currentLine)+'.'+str(self.variant)]) - 1
                    # btnsQtd = len(tempArq['debugCat'][str(self.currentLine)]) - 1
            self.textFont.render_to(surface, self.textRect.topleft, self.lines, (255, 255, 255), (231, 15, 150))

            if not displayedButtons:
                if btnsQtd != 0:
                    for i in range(btnsQtd):
                        displayedButtons[f'btn{i+1}'] = pygame_gui.elements.UIButton(pygame.Rect(150, 200 + 55*i, 100, 50), tempArq['debugCat'][str(self.currentLine)][str(i+1)], uiManager, object_id=str(i+1)) if (len(tempArq['debugCat']) == 1 or self.currentLine == 1) else pygame_gui.elements.UIButton(pygame.Rect(150, 200 + 55*i, 100, 50), tempArq['debugCat'][str(self.currentLine)+'.'+str(self.variant)][str(i+1)], uiManager, object_id=str(i+1))
                        print(displayedButtons)
                else:
                    displayedButtons[f'btn1'] = pygame_gui.elements.UIButton(pygame.Rect(150, 200 + 55, 100, 50), f'Exit', uiManager, object_id=str(1))
        # surface.blit(img, surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2)))
    
    def updateLines(self, btnId : int, displayedButtons : dict):
        with open('.venv/dialogues/debugDialogue.json', 'r') as file:
            tempArq = json.load(file)
        try:
            self.currentLine += 1
            self.variant = btnId
            self.lines = tempArq['debugCat'][str(self.currentLine)+'.'+str(self.variant)]['Dialogue']
        except KeyError:
            self.drawable = False
            self.currentLine = 1
            self.variant = None
            self.lines = ''
            for key in list(displayedButtons.keys()):
                displayedButtons[key].kill()
                del displayedButtons[key]
            return 'normal'

        for key in list(displayedButtons.keys()):
            displayedButtons[key].kill()
            del displayedButtons[key]
        return 'interacting'