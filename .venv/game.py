import sys
import pygame


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen : pygame.Surface = pygame.display.set_mode((640, 360), pygame.RESIZABLE)

        icon : pygame.Surface = pygame.image.load('.venv/images/icon/logo_projecthistoriae.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Project Historiae - Beta')

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.scroll = [0, 0]

    def run(self):
        while True:

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
