import pygame

# CONSTANTS

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0,1), (1,1)]
PHYSICS_TILES = {'grass', 'stone'}
class Tile:
    def __init__(self, tile_type, variant, position):
        self.type = tile_type
        self.variant = variant
        self.position = position 



class Tilemap:
    def __init__(self, game, tile_size=16):
        '''
        This tile map works by mapping a position to a type of tile i.e. (0,0): 'water', (0,1): sky ...
        This is more efficient to work with than a 2D array because in that case we need to define every single position as having something present or not. 
        '''
        self.game = game
        self.tile_size = tile_size 
        self.tilemap = {} # everything on the grid
        self.offgrid_tiles = [] # everything off the grid  - background stuff
        
        # I realize this isn't very enfored so a tile object could be useful
        for i in range(10): 

            self.tilemap[str(3 + i) + ";10"] = Tile(tile_type='grass', variant=1, position=(3 + i, 10))

            self.tilemap['10;' + str(5 + i)] = Tile(tile_type='stone', variant=1, position=(10, 5+i))



    def tiles_around(self, pos):
        '''
        this is really clean. our tilemap has keys as locations, so given a position, we can check if there is a key with that position. Using the NEIGHBOR_OFFSETS constant, we can check the surrounding tiles - if there are nine offsets so we loop through offsets to check nine tiles around the position
        '''

        # convert tile grid position to pixel coordinates
        tiles = []
        tile_location = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))

        for offset in NEIGHBOR_OFFSETS:
            location_lookup = str(tile_location[0] + offset[0]) + ";" + str(tile_location[1] + offset[1])
            if location_lookup in self.tilemap:
                tiles.append(self.tilemap[location_lookup])
        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile.type in PHYSICS_TILES:
                # make a pygame rect for nearby tiles
                # remember every tile has a position and we can multiply by tile_size to get pixel coordinates. We use self.tile_size for the pixel size of the physics rect
                rects.append(pygame.Rect(tile.position[0]* self.tile_size,
                                          tile.position[1]* self.tile_size,
                                          self.tile_size, 
                                          self.tile_size,
                                ))
        return rects

    def render(self, surf, offset):
         
        for tile in self.offgrid_tiles:
            ##surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
            surf.blit(self.game.assets[tile.type][tile.variant], (tile.position[0] - offset[0], tile.position[1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ";" + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile.type ][tile.variant ], (tile.position[0] * self.tile_size - offset[0], tile.position[1] * self.tile_size - offset[1]))


