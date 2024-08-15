import pygame


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen : pygame.Surface = pygame.display.set_mode((640, 360))
        pygame.display.set_caption('Project Historiae Beta')

        self.clock = pygame.time.Clock()

        self.scroll = [0, 0]



# pygame.init()
# pygame.display.set_mode((640, 360))

# running : bool = True

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

# pygame.quit()
