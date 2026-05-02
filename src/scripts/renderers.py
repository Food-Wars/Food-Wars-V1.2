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
                pos = (tile[0][0]*16 - data.camaraXOffset + x*16*8 , tile[0][1]*16 + data.camaraYOffset + y*16*8)

                if tile[1] == 1:
                    surf, coords = data.getImg("terrain", "grass",)
                elif tile[1] == 2:
                    surf, coords = data.getImg("terrain", "water")
                else:
                    #skip if not a valid tile
                    continue
                data.screen.blit(surf, pos, coords)

def getScreenPos(chunk, xOffset, yOffset):
    chunkOffset = (chunk[0] - data.camaraChunk[0], chunk[1] - data.camaraChunk[1])
    #multiply by tile size and chunk size, then add offsets
    #This is based on the map render above, at the time when using the camara chenk (x and y are 0)
    pos = (chunkOffset[0]*8*16 - xOffset - data.camaraXOffset, chunkOffset[1]*8*16 + yOffset + data.camaraYOffset)
    return pos