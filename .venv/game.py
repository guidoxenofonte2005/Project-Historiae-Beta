import sys
import time
import pygame

from gameScripts.utils import *
from gameScripts.entities import Player
from gameScripts.tilemap import Tilemap
from gameScripts.objects import InteractiveObject

from gameScripts.dialogueView import DialogueView

class Game:
    def __init__(self) -> None:
        pygame.init()
    
        self.screen : pygame.Surface = pygame.display.set_mode((640, 360), flags = pygame.RESIZABLE)

        self.display = pygame.Surface((320, 180))

        self.movement : tuple[bool] = [False, False]

        icon : pygame.Surface = pygame.image.load('.venv/images/icon/logo_projecthistoriae.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Project Historiae - Beta')

        self.assets : dict = {
            'player' : load_image('characters/satyr/idle/satyr.png'),
            'marble' : load_images('tiles'),
        }

        self.clock = pygame.time.Clock()

        self.tilemap = Tilemap(self, 32)
        self.tilemap.load('.venv/maps/mapDEBUG.json')

        self.Player = Player(self, 'player', (50, 180), (14, 48))
        self.test = pygame.Rect(self.Player.position[0], self.Player.position[1], self.Player.size[0], self.Player.size[1])

        self.movement = [False, False]

        self.scroll = [0, 0]

        self.dialogueBox = DialogueView("hallo", None)

        self.testCat = InteractiveObject((10, 245), 40, ["dialogue", "get"])
        self.testCatSpr : pygame.Surface = pygame.image.load('.venv/images/catito.png')

    def run(self):
        while True:
            self.display.fill((28, 138, 217))

            self.scroll[0] += (self.Player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 20
            self.scroll[1] += (self.Player.rect().centery - self.display.get_height() / 1.6 - self.scroll[1]) / 15
            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset = renderScroll)

            self.Player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))

            # pygame.draw.rect(self.display, 'white', pygame.Rect(self.Player.position[0] - renderScroll[0], self.Player.position[1] - renderScroll[1], self.Player.size[0], self.Player.size[1]))
            self.Player.render(self.display, offset=renderScroll)

            self.testCat.checkCollision(self.Player, self.display, (self.testCat.position[0] - self.scroll[0] - self.testCat.radius, self.testCat.position[1] - self.scroll[1] - self.testCat.radius))
            
            self.display.blit(self.testCatSpr, (self.testCat.position[0] - self.scroll[0] - self.testCat.radius, self.testCat.position[1] - self.scroll[1] - self.testCat.radius))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_LEFT:
                            self.movement[0] = True
                        case pygame.K_RIGHT:
                            self.movement[1] = True
                        case pygame.K_SPACE:
                            self.Player.jump()
                        case pygame.K_a:
                            self.dialogueBox.update(self.display, (self.Player.position[0] - renderScroll[0], self.Player.position[1] - renderScroll[1]))
                            # self.testCat.interact(self.display, renderScroll, self.dialogueBox)
                if event.type == pygame.KEYUP:
                    match event.key:
                        case pygame.K_LEFT:
                            self.movement[0] = False
                        case pygame.K_RIGHT:
                            self.movement[1] = False
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()
