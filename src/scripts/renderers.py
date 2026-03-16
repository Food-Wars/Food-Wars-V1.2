'''Functions for rendering parts of the world'''

from . import data

def renderMap(screen):
    '''Renders tile background'''
    for y in range(7):
        for x in range(7):
            chunk = data.getChunk(x, y)
            for tile in chunk:
                if tile[1] == 1:
                    screen.blit(data.terrainSprites, (tile[0][0]*16,tile[0][1]*16), (0, 0, 16, 16))
                elif tile[1] == 2:
                    screen.blit(data.terrainSprites, (tile[0][0]*16,tile[0][1]*16), (16, 0, 16, 16))