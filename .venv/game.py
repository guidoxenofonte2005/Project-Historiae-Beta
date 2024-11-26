import sys
import time
import pygame
import pygame_gui
import pyautogui

from gameScripts.utils import *
from gameScripts.entities import Player
from gameScripts.tilemap import Tilemap
from gameScripts.objects import InteractiveObject, LevelSign

from gameScripts.dialogueView import DialogueView, QuizView

from math import sin

import json

class Game:
    def __init__(self) -> None:
        pygame.mixer.pre_init(48000, -16, 2, 1024)
        pygame.init()
    
        self.screen : pygame.Surface = pygame.display.set_mode((0, 0), flags = pygame.RESIZABLE)

        self.guiManager = pygame_gui.UIManager([1920, 1080], ".venv/themes/mainTheme.json")

        self.display = pygame.Surface((320, 180))

        self.movement : tuple[bool] = [False, False]

        icon : pygame.Surface = pygame.image.load('.venv/images/icon/logo_projecthistoriae.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Project Historiae - Beta')

        self.assets : dict = {
            'player/idle' : Animation(load_images('characters/filip/idle'), 18),
            'player/walk' : Animation(load_images('characters/filip/walk'), 12),
            'player/suit' : Animation(load_images('characters/filip/suit'), 22),
            'debugCat' : Animation(load_images('animals/cat1'), 8),
            'debugCat2' : Animation(load_images('animals/cat2')),
            'leftSign' : Animation(load_images('assets/placas/esq')),
            'rightSign' : Animation(load_images('assets/placas/dir')),
            'marble' : load_images('tiles/'),
            'dialogueBox' : load_image('assets/dialogueBox.png'),
            'bkgMenu' : load_image('assets/bkgMenu.png'),
            'title' : load_image('assets/title_with_logo.png'),
            'returnStone' : Animation(load_images('assets/returnStone'), 12),
            'unknownGod' : Animation(load_images('assets/moveisObjetos')),
            'quizLevel' : load_image('assets/auditorium.png'),
            'decor' : load_images('assets/moveis'),

            # npcs
            'oldMan' : Animation(load_images('characters/oldMan'), 50),
            'merchant1' : Animation(load_images('characters/merchant'), 50),
            'merchant2' : Animation(load_images('characters/merchant'), 50),
            'wise' : Animation(load_images('characters/wise'), 50),
            'sacerdote1' : Animation(load_images('characters/wise'), 50),
            'sacerdote2' : Animation(load_images('characters/wise'), 50),

            # bkgs
            'backgroundathens1' : load_image('backgrounds/athens1.png'),
            'backgroundathens2' : load_image('backgrounds/athens2.png'),
            'backgroundathens3' : load_image('backgrounds/athens3.png') # trocar
        }

        self.clock = pygame.time.Clock()

        self.tilemap = Tilemap(self, 32)
        self.tilemap.load('.venv/maps/athens2.json')

        self.Player = Player(self, 'player', (50, 176), (14, 48))
        self.test = pygame.Rect(self.Player.position[0], self.Player.position[1], self.Player.size[0], self.Player.size[1])

        self.movement = [False, False]

        self.scroll = [0, 0]

        # dialogues
        self.dialogueBox = DialogueView('')
        self.quizBox = QuizView('')
        self.correctQuestions : int = 0
        self.questionNum : int = 1
        self.maxQuestions : int = 7
        self.buttonsOnScreen : dict = {}

        self.currentLevel : str = "athens"
        self.levelVar : int = 2
        self.transition : int = 0

        self.interactableObjects = [
            InteractiveObject((10, 245), 37, ["dialogue"], self, 'debugCat'),
            InteractiveObject((80, 245), 41, ["dialogue"], self, 'debugCat2'),
            InteractiveObject((160, 254), 50, ["dialogue"], self, "returnStone"),
            InteractiveObject((220, 214), 50, ["dialogue"], self, "oldMan"),
            InteractiveObject((80, 214), 50, ["dialogue"], self, "merchant1"),
            InteractiveObject((130, 214), 50, ["dialogue"], self, "merchant2"),
            InteractiveObject((280, 201), 40, ["dialogue"], self, "unknownGod"),
            InteractiveObject((100, 210), 50, ['dialogue'], self, "wise"),
            InteractiveObject((100, 210), 50, ['dialogue'], self, "sacerdote1"),
            InteractiveObject((210, 210), 50, ['dialogue'], self, "sacerdote2")
        ]
        self.levelSigns = [
            LevelSign((-70, 203), 40, [], self, "leftSign"),
            LevelSign((350, 200), 40, [], self, "rightSign"),
        ]

        self.objectsPerLevel = {
            1 : [[self.interactableObjects[4], self.interactableObjects[5]], [self.levelSigns[0], self.levelSigns[1]]],
            2 : [[self.interactableObjects[0], self.interactableObjects[2], self.interactableObjects[3], self.interactableObjects[6], self.interactableObjects[7]], [self.levelSigns[0], self.levelSigns[1]]],
            3 : [[self.interactableObjects[8], self.interactableObjects[9]], [self.levelSigns[0]]]
        }

        self.currentPhase : str = 'normal'

        self.ended : bool = False

        self._runMenu_()
    
    def _runMenu_(self):
        #variable set
        runningMenu : bool = True
        angle : float = 0

        #main loop
        while runningMenu:
            angle += 0.1
            time_delta = self.clock.tick(60)/1000.0

            #buttons
            if not self.buttonsOnScreen:
                for i in range(2):
                    match i:
                        case 0:
                            lines = "JOGAR"
                        case 1:
                            lines = "SAIR"
                    tempFont = pygame.font.Font(".venv/fonts/Monocraft.otf", 40) if pyautogui.size()[0] >= 1920 else pygame.font.Font(".venv/fonts/Monocraft.otf", 32)
                    textRect = tempFont.render(lines, True, (0,0,0)).get_rect()
                    btnSize = (textRect.width + 80, 80)
                    self.buttonsOnScreen[f'btn{i+1}'] = pygame_gui.elements.UIButton(pygame.Rect((self.screen.get_width() // 2) - (btnSize[0] // 2), (self.screen.get_height() // 2 + 90)+120*i, btnSize[0], btnSize[1]), lines, self.guiManager, object_id="buttonMenu")

            self.display.blit(self.assets['bkgMenu'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    for label, btn in self.buttonsOnScreen.items():
                        if event.ui_element == btn:
                            match label[-1]:
                                case '1':
                                    runningMenu = False
                                case '2':
                                    pygame.quit()
                                    sys.exit()

            self.guiManager.process_events(event)

            self.guiManager.update(time_delta)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.screen.blit(pygame.transform.scale(self.assets['title'], [self.screen.get_size()[0] // 1.4, self.screen.get_size()[1] // 1.6]), (self.screen.get_size()[0] // 7, 0 + 2*sin(angle)))
            
            self.guiManager.draw_ui(self.screen)

            pygame.display.update()

        for key in list(self.buttonsOnScreen.keys()):
            self.buttonsOnScreen[key].kill()
            del self.buttonsOnScreen[key]

        self.transition = -30
        self._runTransition_()

    def loadLevel(self, pastLevelId : int, direction : int, customDirection : int = 0) -> None:
        match direction:
            case 1:
                self.tilemap.load(f".venv/maps/{self.currentLevel}{str(pastLevelId + 1)}.json")
                self.levelVar = pastLevelId + 1
                self.Player.position[0] = self.levelSigns[0].position[0]
            case -1:
                self.tilemap.load(f".venv/maps/{self.currentLevel}{str(pastLevelId - 1)}.json")
                self.levelVar = pastLevelId - 1
                self.Player.position[0] = self.levelSigns[1].position[0]
            case _:
                self.tilemap.load(f".venv/maps/{self.currentLevel}{str(pastLevelId + customDirection)}.json")
                self.levelVar = pastLevelId + customDirection
        self.transition = -30

    def run(self):
        pygame.mixer.music.load('.venv/music/menuSong.wav')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        while not self.ended:
            match self.currentPhase:
                case 'finalQuiz':
                    time_delta = self.clock.tick(60)/1000.0

                    self.display.blit(self.assets['quizLevel'], (-20, -20))
                    
                    if self.transition < 0:
                        self.transition += 1

                    self.Player.position = [230, 79]
                    self.Player.flip = True

                    self.Player.setAction('suit')

                    self.Player.animation.update()
                    self.Player.render(self.display)

                    self.tilemap.render(self.display)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            match event.key:
                                case pygame.K_LEFT:
                                    if self.currentPhase != 'interacting':
                                        self.movement[0] = True
                                case pygame.K_RIGHT:
                                    if self.currentPhase != 'interacting':
                                        self.movement[1] = True
                        if event.type == pygame.KEYUP:
                            match event.key:
                                case pygame.K_LEFT:
                                    self.movement[0] = False
                                case pygame.K_RIGHT:
                                    self.movement[1] = False
                        if event.type == pygame_gui.UI_BUTTON_PRESSED:
                            for label, btn in self.buttonsOnScreen.copy().items():
                                if event.ui_element == btn:
                                    with open('.venv/questions/athens.json', 'r') as file:  
                                        tempArq = json.load(file)
                                    if tempArq[str(self.questionNum)][str(int(label[-1]))]["Answer"] == True:
                                        self.correctQuestions += 1
                                        sfx = pygame.mixer.Sound('.venv/music/CorrectSfx.wav')
                                    else:
                                        sfx = pygame.mixer.Sound('.venv/music/WrongSfx.wav')
                                    sfx.play(loops=0)
                                    pygame.time.wait(500)
                                    sfx.stop()

                                    self.quizBox.updateLines(int(label[-1]), self.buttonsOnScreen)
                                    self.questionNum += 1
                        self.guiManager.process_events(event)
                    
                    if self.questionNum == self.maxQuestions + 1:
                        self.ended = True
                    
                    self.guiManager.update(time_delta)
                    
                    if self.transition:
                        self._runTransition_()

                    self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                    
                    if self.transition == 0:
                        self.quizBox.drawable = True
                        self.screen.blit(pygame.transform.scale(self.assets['dialogueBox'], [self.screen.get_size()[0] // 2, self.screen.get_size()[1] // 3]), (self.screen.get_width() // 4, 0))

                        self.quizBox.draw(self.screen, self.Player, self.guiManager, self.buttonsOnScreen)
                        self.guiManager.draw_ui(self.screen)

                    pygame.display.update()
                case _:
                    time_delta = self.clock.tick(60)/1000.0

                    self.display.fill((28, 138, 217))

                    self.scroll[0] += (self.Player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 20
                    self.scroll[1] += (self.Player.rect().centery - self.display.get_height() / 1.6 - self.scroll[1]) / 15

                    self.testScroll = max(-145, min(self.scroll[0], 70))

                    if self.levelVar == 1:
                        self.display.blit(pygame.transform.scale(self.assets[f'background{self.currentLevel}{self.levelVar}'], [560, 180]), (-160 - self.testScroll, 2))
                    else:
                        self.display.blit(self.assets[f'background{self.currentLevel}{self.levelVar}'], (-140 - self.testScroll, 2))
                    
                    renderScroll = (int(self.testScroll), int(self.scroll[1]))

                    match self.currentPhase:
                        case 'interacting':
                            self.Player.movable = False
                        case 'normal':
                            self.Player.movable = True
                    
                    if self.transition < 0:
                        self.transition += 1

                    self.tilemap.render(self.display, offset = renderScroll)

                    self.Player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                    self.Player.render(self.display, offset=renderScroll)

                    for i in range(len(self.objectsPerLevel[self.levelVar][0])):
                        self.dialogueBox.drawable = True if self.objectsPerLevel[self.levelVar][0][i].checkCollision(self.Player, self.display, (self.objectsPerLevel[self.levelVar][0][i].position[0] - self.testScroll - self.objectsPerLevel[self.levelVar][0][i].radius, self.objectsPerLevel[self.levelVar][0][i].position[1] - self.scroll[1] - self.objectsPerLevel[self.levelVar][0][i].radius)) else False
                        if self.dialogueBox.drawable:
                            break
                    
                    for i in range(len(self.objectsPerLevel[self.levelVar][0])):
                        self.objectsPerLevel[self.levelVar][0][i].render(self.display, offset=[self.testScroll, renderScroll[1]])
                        self.objectsPerLevel[self.levelVar][0][i].animation.update()
                    
                    for i in range(len(self.objectsPerLevel[self.levelVar][1])):
                        if self.levelVar == 1:
                            self.objectsPerLevel[self.levelVar][1][i].checkCollision(self.Player, self.display, (self.objectsPerLevel[self.levelVar][1][1].position[0] - self.testScroll - self.objectsPerLevel[self.levelVar][1][1].radius, self.objectsPerLevel[self.levelVar][1][1].position[1] - self.scroll[1] - self.objectsPerLevel[self.levelVar][1][1].radius))
                        else:
                            self.objectsPerLevel[self.levelVar][1][i].checkCollision(self.Player, self.display, (self.objectsPerLevel[self.levelVar][1][i].position[0] - self.testScroll - self.objectsPerLevel[self.levelVar][1][i].radius, self.objectsPerLevel[self.levelVar][1][i].position[1] - self.scroll[1] - self.objectsPerLevel[self.levelVar][1][i].radius))

                    for i in range(len(self.objectsPerLevel[self.levelVar][1])):
                        if self.levelVar == 1:
                            self.objectsPerLevel[self.levelVar][1][1].render(self.display, offset=[self.testScroll, renderScroll[1]])
                            self.objectsPerLevel[self.levelVar][1][1].animation.update()
                        else:
                            self.objectsPerLevel[self.levelVar][1][i].render(self.display, offset=[self.testScroll, renderScroll[1]])
                            self.objectsPerLevel[self.levelVar][1][i].animation.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            match event.key:
                                case pygame.K_LEFT:
                                    if self.currentPhase != 'interacting':
                                        self.movement[0] = True
                                case pygame.K_RIGHT:
                                    if self.currentPhase != 'interacting':
                                        self.movement[1] = True
                                case pygame.K_a:
                                    if self.currentPhase != 'interacting':
                                        for i in range(len(self.objectsPerLevel[self.levelVar][0])):
                                            lastPhase = self.currentPhase
                                            self.currentPhase = self.objectsPerLevel[self.levelVar][0][i].interact(self.display, [self.testScroll, renderScroll[1]], self.dialogueBox, phase=self.currentPhase)
                                            if self.currentPhase != lastPhase:
                                                self.dialogueBox._setNpc_(self.objectsPerLevel[self.levelVar][0][i].name)
                                                break
                                        if self.levelVar == 1:
                                            for i in range(len(self.objectsPerLevel[self.levelVar][1])):
                                                self.objectsPerLevel[self.levelVar][1][1].interact(None, None, None, None)
                                        else:
                                            for i in range(len(self.objectsPerLevel[self.levelVar][1])):
                                                self.objectsPerLevel[self.levelVar][1][i].interact(None, None, None, None)
                        if event.type == pygame.KEYUP:
                            match event.key:
                                case pygame.K_LEFT:
                                    self.movement[0] = False
                                case pygame.K_RIGHT:
                                    self.movement[1] = False
                        if event.type == pygame_gui.UI_BUTTON_PRESSED:
                            for label, btn in self.buttonsOnScreen.copy().items():
                                if event.ui_element == btn:
                                    self.currentPhase = self.dialogueBox.updateLines(int(label[-1]), self.buttonsOnScreen)
                                    interactingObject = next((obj for obj in self.interactableObjects if obj.interactable), None)
                                    if interactingObject.name == "returnStone":
                                        if int(label[-1]) == 1:
                                            self.currentPhase = 'changeAreaToQuiz'
                                    sfx = pygame.mixer.Sound('.venv/music/BtnClickSfx.wav')
                                    sfx.play()
                                    pygame.time.wait(100)
                                    sfx.stop()

                        self.guiManager.process_events(event)
                    
                    self.guiManager.update(time_delta)
                    
                    if self.currentPhase[:10] == 'changeArea':
                        if self.transition <= 30:
                            self.transition += 1
                        else:
                            self.transition = -30
                            if self.currentPhase == 'changeAreaToQuiz':
                                self.currentPhase = 'finalQuiz'
                                self.tilemap.load(f".venv/maps/finalQuiz.json")
                                pygame.mixer.music.stop()
                                pygame.mixer.music.load('.venv/music/quiz.wav')
                                pygame.mixer.music.set_volume(0.4)
                                pygame.mixer.music.play(-1)
                    if self.transition:
                        self._runTransition_()

                    self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

                    if self.dialogueBox.drawable:
                        if self.currentPhase == 'interacting':
                            self.screen.blit(pygame.transform.scale(self.assets['dialogueBox'], [self.screen.get_size()[0] // 2, self.screen.get_size()[1] // 3]), (self.screen.get_width() // 4, 0))

                        self.dialogueBox.draw(self.screen, self.Player, self.guiManager, self.buttonsOnScreen)
                        self.guiManager.draw_ui(self.screen)

                    pygame.display.update()

        while True:
            if not self.buttonsOnScreen:
                lines = "SAIR"
                tempFont = pygame.font.Font(".venv/fonts/Monocraft.otf", 40) if pyautogui.size()[0] >= 1920 else pygame.font.Font(".venv/fonts/Monocraft.otf", 32)
                textRect = tempFont.render(lines, True, (0,0,0)).get_rect()
                btnSize = (textRect.width + 80, 80)
                self.buttonsOnScreen[f'btn{i+1}'] = pygame_gui.elements.UIButton(pygame.Rect((self.screen.get_width() // 2) - (btnSize[0] // 2), (self.screen.get_height() // 2 + 200), btnSize[0], btnSize[1]), lines, self.guiManager, object_id="buttonMenu")

            self.display.blit(self.assets['bkgMenu'])

            text = f'Thanks for playing! >:D\nYour score was {self.correctQuestions}.'
            font = pygame.freetype.SysFont("Monocraft", 24) if pyautogui.size()[0] >= 1920 else pygame.freetype.SysFont("Monocraft", 16)
            tempFont = pygame.font.Font(".venv/fonts/Monocraft.otf", 24) if pyautogui.size()[0] >= 1920 else pygame.font.Font(".venv/fonts/Monocraft.otf", 16)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    for label, btn in self.buttonsOnScreen.items():
                        if event.ui_element == btn:
                            pygame.quit()
                            sys.exit()

            self.guiManager.process_events(event)

            self.guiManager.update(time_delta)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.screen.blit(pygame.transform.scale(self.assets['title'], [self.screen.get_size()[0] // 1.4, self.screen.get_size()[1] // 1.6]), (self.screen.get_size()[0] // 7, 0))

            index = 0
            for word in text.splitlines():
                tempRect : pygame.Rect = tempFont.render(word, True, (0,0,0)).get_rect()
                font.render_to(self.screen, [self.screen.get_width() // 2 - tempRect.centerx, (self.screen.get_height() // 2 + 80) + 30 * index], word, (255, 255, 255))
                index += 1
            
            self.guiManager.draw_ui(self.screen)

            pygame.display.update()

    def _runTransition_(self):
        transition_surf = pygame.Surface(self.display.get_size())
        pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
        transition_surf.set_colorkey((255, 255, 255))
        self.display.blit(transition_surf, (0, 0))

Game().run()