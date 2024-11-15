import sys
import time
import pygame
import pygame_gui
import pyautogui

from gameScripts.utils import *
from gameScripts.entities import Player
from gameScripts.tilemap import Tilemap
from gameScripts.objects import InteractiveObject

from gameScripts.dialogueView import DialogueView, QuizView

from math import sin

class Game:
    def __init__(self) -> None:
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
            'marble' : load_images('tiles/'),
            'dialogueBox' : load_image('assets/dialogueBox.png'),
            'bkgMenu' : load_image('assets/bkgMenu.png'),
            'title' : load_image('assets/title_with_logo.png'),
            'returnStone' : Animation(load_images('assets/returnStone'), 12),
            'quizLevel' : load_image('assets/auditorium.png'),
            'teachDesk' : load_image('assets/desk.png'),
        }

        self.clock = pygame.time.Clock()

        self.tilemap = Tilemap(self, 32)
        self.tilemap.load('.venv/maps/mapDEBUG.json')

        self.Player = Player(self, 'player', (50, 176), (14, 48))
        self.test = pygame.Rect(self.Player.position[0], self.Player.position[1], self.Player.size[0], self.Player.size[1])

        self.movement = [False, False]

        self.scroll = [0, 0]

        # dialogues
        self.dialogueBox = DialogueView('')
        self.quizBox = QuizView('')
        self.correctQuestions : int = 0
        self.buttonsOnScreen : dict = {}

        self.currentLevel : str
        self.levelVar : int
        self.transition : int = 0

        self.interactableObjects = [
            InteractiveObject((10, 245), 37, ["dialogue"], self, 'debugCat'),
            InteractiveObject((80, 245), 41, ["dialogue"], self, 'debugCat2'),
            InteractiveObject((160, 254), 50, ["dialogue"], self, "returnStone")
        ]

        self.currentPhase : str = 'normal'

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
                    tempFont = pygame.font.Font(".venv/fonts/Monocraft.ttf", 40) if pyautogui.size()[0] >= 1920 else pygame.font.Font(".venv/fonts/Monocraft.ttf", 32)
                    textRect = tempFont.render(lines, True, (0,0,0)).get_rect()
                    btnSize = (textRect.width + 80, 80)
                    self.buttonsOnScreen[f'btn{i+1}'] = pygame_gui.elements.UIButton(pygame.Rect((self.screen.get_width() // 2) - (btnSize[0] // 2), (self.screen.get_height() // 2 + 90)+120*i, btnSize[0], btnSize[1]), lines, self.guiManager, object_id="buttonMenu")
                print(self.buttonsOnScreen)

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
            case -1:
                self.tilemap.load(f".venv/maps/{self.currentLevel}{str(pastLevelId - 1)}.json")
                self.levelVar = pastLevelId - 1
            case _:
                self.tilemap.load(f".venv/maps/{self.currentLevel}{str(pastLevelId + customDirection)}.json")
                self.levelVar = pastLevelId + customDirection
        self.transition = -30

    def __loadCustomLevel__(self, levelName):
        self.tilemap.load(f".venv/maps/{levelName}.json")
        self.transition = -30

    def run(self):
        while True:
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

                    self.display.blit(self.assets['teachDesk'], (220, 107))

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
                                print(label, btn)
                                if event.ui_element == btn:
                                    print(self.currentPhase)
                                    self.currentPhase = self.quizBox.updateLines(int(label[-1]), self.buttonsOnScreen)
                        self.guiManager.process_events(event)
                    
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
                case 'endGame':
                    pass
                case _:
                    time_delta = self.clock.tick(60)/1000.0
                    self.display.fill((28, 138, 217))

                    self.scroll[0] += (self.Player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 20
                    self.scroll[1] += (self.Player.rect().centery - self.display.get_height() / 1.6 - self.scroll[1]) / 15
                    renderScroll = (int(self.scroll[0]), int(self.scroll[1]))

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

                    for i in range(len(self.interactableObjects)):
                        self.dialogueBox.drawable = True if self.interactableObjects[i].checkCollision(self.Player, self.display, (self.interactableObjects[i].position[0] - self.scroll[0] - self.interactableObjects[i].radius, self.interactableObjects[i].position[1] - self.scroll[1] - self.interactableObjects[i].radius)) else False
                        if self.dialogueBox.drawable:
                            break
                    
                    for i in range(len(self.interactableObjects)):
                        self.interactableObjects[i].render(self.display, offset=renderScroll)
                        self.interactableObjects[i].animation.update()

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
                                    # self.dialogueBox.update(self.display, (self.Player.position[0] - renderScroll[0], self.Player.position[1] - renderScroll[1]))
                                    for i in range(len(self.interactableObjects)):
                                        lastPhase = self.currentPhase
                                        self.currentPhase = self.interactableObjects[i].interact(self.display, renderScroll, self.dialogueBox, phase=self.currentPhase)
                                        if self.currentPhase != lastPhase:
                                            self.dialogueBox._setNpc_(self.interactableObjects[i].name)
                                            break
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
                                    if interactingObject.name == "returnStone" and label[-1] == "1":
                                        self.currentPhase = 'changeAreaToQuiz'

                        self.guiManager.process_events(event)
                    
                    self.guiManager.update(time_delta)
                    
                    if self.currentPhase[:10] == 'changeArea':
                        if self.transition <= 30:
                            self.transition += 1
                        else:
                            self.transition = -30
                            if self.currentPhase == 'changeAreaToQuiz':
                                self.currentPhase = 'finalQuiz'
                    if self.transition:
                        self._runTransition_()

                    self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

                    if self.dialogueBox.drawable:
                        if self.currentPhase == 'interacting':
                            self.screen.blit(pygame.transform.scale(self.assets['dialogueBox'], [self.screen.get_size()[0] // 2, self.screen.get_size()[1] // 3]), (self.screen.get_width() // 4, 0))

                        self.dialogueBox.draw(self.screen, self.Player, self.guiManager, self.buttonsOnScreen)
                        self.guiManager.draw_ui(self.screen)

                    pygame.display.update()

    def _runTransition_(self):
        transition_surf = pygame.Surface(self.display.get_size())
        pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
        transition_surf.set_colorkey((255, 255, 255))
        self.display.blit(transition_surf, (0, 0))

Game().run()