import sys
import pygame

from gameScripts.utils import *
from gameScripts.entities import Player
from gameScripts.tilemap import Tilemap

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen : pygame.Surface = pygame.display.set_mode((640, 360), pygame.RESIZABLE)

        self.display = pygame.Surface((640, 360))

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
        self.tilemap.load('.venv/maps/map.json')

        self.Player = Player(self, 'player', (50, 50), (14, 48))
        self.test = pygame.Rect(self.Player.position[0], self.Player.position[1], self.Player.size[0], self.Player.size[1])

        self.movement = [False, False]

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.screen.fill((28, 138, 217))

            self.scroll[0] += (self.Player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 20
            self.scroll[1] += (self.Player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 15
            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.screen, offset = renderScroll)

            self.test = pygame.Rect(self.Player.position[0] - renderScroll[0], self.Player.position[1] - renderScroll[1], self.Player.size[0], self.Player.size[1])
            pygame.draw.rect(self.screen, (255, 255, 255), self.test)
            self.Player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.Player.render(self.screen, offset=renderScroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()
            self.clock.tick(60)

Game().run()

# pygame.init()
# pygame.display.set_mode((640, 360))

# running : bool = True

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

# pygame.quit()
