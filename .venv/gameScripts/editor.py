import sys
import pygame

from gameScripts.utils import load_images
from gameScripts.tilemap import Tilemap

RENDER_SCALE = 1.0

class Editor:
    def __init__(self) -> None:
        pygame.init()
        
        self.screen : pygame.Surface = pygame.display.set_mode((640, 360))
        pygame.display.set_caption("Tile Editor")

        self.display = pygame.Surface((640, 360))
        
        self.clock = pygame.time.Clock()

        self.movement : tuple[bool] = [False, False, False, False]

        self.assets : dict = {
            'marble' : load_images('tiles/')
        }

        self.tileMap = Tilemap(self, tileSize=32)


        try:
            self.tileMap.load('.venv/maps/mapDEBUG.json')
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        self.on_grid = True
        
        self.left_clicking = False
        self.right_clicking = False
        self.shift = False

    def run(self):

        while True:
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tileMap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            mouse_position = pygame.mouse.get_pos()
            mouse_position = (mouse_position[0] / RENDER_SCALE, mouse_position[1] / RENDER_SCALE)
            tile_position = (int(mouse_position[0] + self.scroll[0]) // self.tileMap.tile_size, int(mouse_position[1] + self.scroll[1]) // self.tileMap.tile_size)

            if self.on_grid:
                self.display.blit(current_tile_img, (tile_position[0] * self.tileMap.tile_size - self.scroll[0], tile_position[1] * self.tileMap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mouse_position)

            if self.left_clicking and self.on_grid:
                self.tileMap.tilemap[str(tile_position[0]) + ";" + str(tile_position[1])] = {"type" : self.tile_list[self.tile_group], "variant" : self.tile_variant, "pos" : tile_position}
            if self.right_clicking:
                tile_location = str(tile_position[0]) + ";" + str(tile_position[1])
                if tile_location in self.tileMap.tilemap:
                    del self.tileMap.tilemap[tile_location]
                for tile in self.tileMap.offgrid_tiles.copy():
                    tile_image = self.assets[tile['type']]
                    tile_hitbox = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_image.get_width(), tile_image.get_height())
                    if tile_hitbox.collidepoint(mouse_position):
                        self.tileMap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.left_clicking = True
                        if not self.on_grid:
                            self.tileMap.offgrid_tiles.append({"type" : self.tile_list[self.tile_group], 'variant' : self.tile_variant, 'pos' : (mouse_position[0] + self.scroll[0], mouse_position[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    match event.button:
                        case 1:
                            self.left_clicking = False
                        case 3:
                            self.right_clicking = False
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_a:
                            self.movement[0] = True
                        case pygame.K_d:
                            self.movement[1] = True
                        case pygame.K_w:
                            self.movement[2] = True
                        case pygame.K_s:
                            self.movement[3] = True
                        case pygame.K_o:
                            self.tileMap.save('.venv/maps/mapDEBUG.json')
                        case pygame.K_t:
                            self.tileMap.autotile()
                        case pygame.K_g:
                            self.on_grid = not self.on_grid
                        case pygame.K_LSHIFT:
                            self.shift = True
                if event.type == pygame.KEYUP:
                    match event.key:
                        case pygame.K_a:
                            self.movement[0] = False
                        case pygame.K_d:
                            self.movement[1] = False
                        case pygame.K_w:
                            self.movement[2] = False
                        case pygame.K_s:
                            self.movement[3] = False
                        case pygame.K_LSHIFT:
                            self.shift = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()