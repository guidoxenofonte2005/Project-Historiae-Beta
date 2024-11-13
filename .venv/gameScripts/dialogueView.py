import pygame
import time
import pygame.freetype
import pygame_gui

import pyautogui

import json
# classe pra lidar com diálogos
# ainda falta pensar em como isso funcionaria
class DialogueView:
    def __init__(self, lines : str = '') -> None:
        if '\n' in lines:
            self.lines = lines.split("\n")
        else:
            self.lines = lines
        self.npc = ''
        self.textFont = pygame.freetype.SysFont("Monocraft", 24) if pyautogui.size()[0] >= 1920 else pygame.freetype.SysFont("Monocraft", 16)

        if type(self.lines) == list:
            self.textRect = self.textFont.get_rect(self.lines[0])
        else:
            self.textRect = self.textFont.get_rect(self.lines)

        self.drawable : bool = False

        self.dialogueFile = ''

        self.currentLine : int = 1
        self.variant : int = None
    
    def _setNpc_(self, newNpc : str):
        self.npc = newNpc

    def draw(self, surface : pygame.Surface, player, uiManager, displayedButtons : dict):
        if self.lines != "":
            if "\n" in self.lines:
                lineCollection = self.lines.splitlines()
            else:
                lineCollection = []
            
            # turn off player movement
            player.movable = False

            with open('.venv/dialogues/debugDialogue.json', 'r') as file:
                tempArq = json.load(file)
                if len(tempArq[self.npc]) == 1 or self.currentLine == 1:
                    btnsQtd = len(tempArq[self.npc][str(self.currentLine)]) - 1
                else:
                    btnsQtd = len(tempArq[self.npc][str(self.currentLine)+'.'+str(self.variant)]) - 1

            # line handling
            if len(lineCollection) <= 1:
                self.textFont.render_to(surface, [surface.get_width() // 4 + 68, 30], self.lines, (255, 255, 255))
            else:
                index = 0
                for word in lineCollection:
                    self.textFont.render_to(surface, [surface.get_width() // 4 + 68, 30 + 30 * index], word, (255, 255, 255))
                    index += 1

            if not displayedButtons:
                if btnsQtd != 0:
                    for i in range(btnsQtd):
                        tempFont = pygame.font.Font(".venv/fonts/Monocraft.ttf", 24) if pyautogui.size()[0] >= 1920 else pygame.font.Font(".venv/fonts/Monocraft.ttf", 16)
                        textRect = tempFont.render(tempArq[self.npc][str(self.currentLine)][str(i+1)], True, (0,0,0)).get_rect()
                        btnSize = (textRect.width + 10, 30)
                        displayedButtons[f'btn{i+1}'] = pygame_gui.elements.UIButton(pygame.Rect((surface.get_size()[0] * 5) // 9, (surface.get_size()[1] // 5)+30*i, btnSize[0], btnSize[1]), tempArq[self.npc][str(self.currentLine)][str(i+1)], uiManager, object_id="buttonDialogue") if (len(tempArq[self.npc]) == 1 or self.currentLine == 1) else pygame_gui.elements.UIButton(pygame.Rect((surface.get_size()[0] * 5) // 8, (surface.get_size()[1] // 5)+30*i, btnSize[0], btnSize[1]), tempArq[self.npc][str(self.currentLine)+'.'+str(self.variant)][str(i+1)], uiManager, object_id="buttonDialogue")
                else:
                    displayedButtons[f'btn1'] = pygame_gui.elements.UIButton(pygame.Rect((surface.get_size()[0] * 5) // 8, surface.get_size()[1] // 5, 70, 30), f'Exit', uiManager, object_id="buttonDialogue")
        # surface.blit(img, surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2)))
    
    def updateLines(self, btnId : int, displayedButtons : dict):
        with open('.venv/dialogues/debugDialogue.json', 'r') as file:
            tempArq = json.load(file)
        try:
            self.currentLine += 1
            self.variant = btnId
            self.lines = tempArq[self.npc][str(self.currentLine)+'.'+str(self.variant)]['Dialogue']
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