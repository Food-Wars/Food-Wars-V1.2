import opensimplex

seed = 0
chunk_size = 8

def defineSeed(newSeed):
    global seed
    seed = newSeed


def generateChunk(x, y):
    chunk_data = []
    #set up noise generator
    opensimplex.seed(seed)
    #iterate through each tile in the chunk
    for yPos in range(chunk_size):
        for xPos in range(chunk_size):
            #find x and y locations
            targetX = x * chunk_size + xPos
            targetY = y * chunk_size + yPos
            #defult tile is nothing
            tileType = 0
            height = opensimplex.noise2(targetX / 30, targetY / 30)
            #use height to determine tile type
            #2 = water
            #1 = grass
            if height <= -0.3:
                tileType = 2
                #set interactabl;e item to zero because tile is water
            elif height > -0.3:
                tileType = 1
            if tileType != 0:
                #if the tile is not nothing, add it to the chunk data
                chunk_data.append([(xPos, yPos), tileType])
    return chunk_data