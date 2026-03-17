'''Functions for rendering parts of the world'''

from . import data

def renderMap():
    '''Renders tile background'''

    for y in range(-1, 8):
        for x in range(-1, 8):
            chunk = data.getChunk(x + data.camaraChunk[0], y + data.camaraChunk[1])
            for tile in chunk:

                #calcualte position using tile coords and camara offsets
                #tile images are 16x16, multiply by 16 so they don't overlap each other
                #x*16*8 -> multiply by tiles per chunk, then by size of chunk
                pos = (tile[0][0]*16 - data.camaraXOffest + x*16*8 , tile[0][1]*16 + data.camaraYOffest + y*16*8)

                if tile[1] == 1:
                    data.screen.blit(data.terrainSprites, pos, (0, 0, 16, 16))
                elif tile[1] == 2:
                    data.screen.blit(data.terrainSprites, pos, (16, 0, 16, 16))