import sys
import time
import pygame

from gameScripts.utils import *
from gameScripts.entities import Player
from gameScripts.tilemap import Tilemap
from gameScripts.objects import InteractiveObject

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
            'player' : load_image('characters/satyr_test.png'),
            'marble' : load_image('tiles/floor_shit.png'),
        }

        self.clock = pygame.time.Clock()

        self.tilemap = Tilemap(self, 32)
        self.tilemap.load('.venv/maps/mapDEBUG.json')

        self.Player = Player(self, 'player', (50, 180), (14, 48))
        self.test = pygame.Rect(self.Player.position[0], self.Player.position[1], self.Player.size[0], self.Player.size[1])

        self.movement = [False, False]

        self.scroll = [0, 0]
        
        self.textFont = pygame.font.SysFont("smwwholepixelspacingregular", 20)

        self.testCat = InteractiveObject((10, 245), radius = 40)
        self.testCatSpr : pygame.Surface = pygame.image.load('.venv/images/catito.png')

    def run(self):
        while True:
            self.display.fill((28, 138, 217))

            self.scroll[0] += (self.Player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 20
            self.scroll[1] += (self.Player.rect().centery - self.display.get_height() / 1.6 - self.scroll[1]) / 15
            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset = renderScroll)

            self.Player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
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
                        case pygame.K_F11:
                            pygame.display.toggle_fullscreen()
                if event.type == pygame.KEYUP:
                    match event.key:
                        case pygame.K_LEFT:
                            self.movement[0] = False
                        case pygame.K_RIGHT:
                            self.movement[1] = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

            # print("")
            # print(self.testInteractableObject.position)
            # print(self.Player.position)
            # print(self.Player.rect().center)
            # print(self.Player.position)
            # print(self.tilemap.tiles_around(self.Player.position))
            # print(self.tilemap.physics_rects_around(self.Player.position))
            # time.sleep(0.1)

Game().run()

# pygame.init()
# pygame.display.set_mode((640, 360))

# running : bool = True

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

# pygame.quit()
