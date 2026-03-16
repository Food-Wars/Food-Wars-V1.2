'''This is a file for storing global data from files'''

import os

import pygame

from . import worldGen

#image data
icon = None
terrainSprites = None

#world data
chunks = {}

#camara data
camaraChunk = [0, 0]
camaraXOffest = 0
camaraYOffest = 0

#funtions
def loadIcon():
    global icon
    icon = pygame.image.load(os.path.join("game_files", "imgs", "gui", "cupcake_icon.png"))

def loadImages():
    global terrainSprites
    terrainSprites = pygame.image.load(os.path.join("game_files", "imgs", "tiles", "tiles_background.png"))
    terrainSprites.convert() #reccomended for blit speed

def getChunk(x, y):
    if (x, y) in chunks.keys():
        return chunks[(x, y)]
    chunks[(x, y)] = worldGen.generateChunk(x, y)
    return chunks[(x, y)]