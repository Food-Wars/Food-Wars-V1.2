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
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            #find x and y locations
            target_x = x * chunk_size + x_pos
            target_y = y * chunk_size + y_pos
            #defult tile is nothing
            tile_type = 0
            height = opensimplex.noise2(target_x / 30, target_y / 30)
            #use height to determine tile type
            #2 = water
            #1 = grass
            if height <= -0.3:
                tile_type = 2
                #set interactabl;e item to zero because tile is water
            elif height > -0.3:
                tile_type = 1
            if tile_type != 0:
                #if the tile is not nothing, add it to the chunk data
                chunk_data.append([(target_x, target_y), tile_type])
    return chunk_data