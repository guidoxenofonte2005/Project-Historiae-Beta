import json
import pygame

# AUTOTILE_MAP = {
#     tuple(sorted([(1, 0), (0, 1)])) : 0,
#     tuple(sorted([(1, 0), (0, 1), (-1, 0)])) : 1,
#     tuple(sorted([(-1, 0), (0, 1)])) : 2,
#     tuple(sorted([(-1, 0), (0, -1), (0, 1)])) : 3,
#     tuple(sorted([(-1, 0), (0, -1)])) : 4,
#     tuple(sorted([(-1, 0), (0, -1), (1, 0)])) : 5,
#     tuple(sorted([(1, 0), (0, -1)])) : 6,
#     tuple(sorted([(1, 0), (0, -1), (0, 1)])) : 7,
#     tuple(sorted([(-1, 0), (0, -1), (0, 1), (1, 0)])) : 8,
#     tuple(sorted([(-1, 0)])) : 2,
#     tuple(sorted([(1, 0)])) : 0,
#     tuple(sorted([(0, -1)])) : 8,
#     tuple(sorted([(0, 1)])) : 1
# }

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1), (0, 2), (2, 0), (0, -2), (-2, 0)]
PHYSICS_TILES = {'marble', }
# AUTOTILE_TYPES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tileSize : int = 32) -> None:
        self.game = game
        self.tile_size = tileSize
        self.tilemap = {}
        self.offgrid_tiles = []

    def extract(self, id_pairs, keep = False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for location in self.tilemap.copy():
            tile = self.tilemap[location]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[location]

        return matches
    
    def tiles_around(self, position, e_offset = (0, 0)) -> list:
        tiles : list = []

        tile_location = (int((position[0] + e_offset[0]) // self.tile_size) , int((position[1] + e_offset[1]) // self.tile_size))
        
        for offset in NEIGHBOR_OFFSETS:
            check_location : str = str(tile_location[0] + offset[0]) + ';' + str(tile_location[1] + offset[1])
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])

        return tiles

    # def autotile(self):
    #     for location in self.tilemap:
    #         tile = self.tilemap[location]
    #         neighbours = set()
    #         for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
    #             check_location = str(tile['pos'][0] + shift[0]) + ";" + str(tile['pos'][1] + shift[1])
    #             if check_location in self.tilemap:
    #                 if self.tilemap[check_location]['type'] == tile['type']:
    #                     neighbours.add(shift)
    #         neighbours = tuple(sorted(neighbours))
    #         if (tile['type'] in AUTOTILE_TYPES) and (neighbours in AUTOTILE_MAP):
    #             tile['variant'] = AUTOTILE_MAP[neighbours]
    
    def physics_rects_around(self, position, offset = (0, 0)) -> list:
        rects : list = []

        for tile in self.tiles_around(position, offset):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))

        return rects

    def render(self, destination : pygame.Surface, offset = (0, 0)):
        for tile in self.offgrid_tiles:
            destination.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        
        # for x in range(offset[0] // self.tile_size, (offset[0] + destination.get_width()) // self.tile_size + 1):
        #     for y in range(offset[1] // self.tile_size, (offset[1] + destination.get_height()) // self.tile_size + 1):
        #         location = str(x) + ";" + str(y)
        #         if location in self.tilemap:
        #             tile = self.tilemap[location]
        #             destination.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
        # versão não otimizada do código de renderização
        for location in self.tilemap:
            tile = self.tilemap[location]
            destination.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap' : self.tilemap, 'tile_size' : self.tile_size, 'offgrid' : self.offgrid_tiles}, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        mapData = json.load(f)
        f.close()

        self.tilemap = mapData['tilemap']
        self.tile_size = mapData['tile_size']
        self.offgrid_tiles = mapData['offgrid']
