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

def move(directions):
    global camaraChunk
    global camaraXOffest
    global camaraYOffest

    #directions storead as (w, a, s, d)
    if directions[0]:
        camaraYOffest += 5
    elif directions[2]:
        camaraYOffest -= 5
    if directions[1]:
        camaraXOffest -= 5
    elif directions[3]:
        camaraXOffest += 5
    
    #handle moving chunks
    if camaraYOffest > 128:
        camaraChunk[1] -= 1
        camaraYOffest = 0 + (camaraYOffest - 128)
    elif camaraYOffest < 0:
        camaraChunk[1] += 1
        camaraYOffest = 128 + camaraYOffest #already negative

    if camaraXOffest > 128:
        camaraChunk[0] += 1
        camaraXOffest = 0 + (camaraXOffest - 128)
    elif camaraXOffest < 0:
        camaraChunk[0] -= 1
        camaraXOffest = 128 + camaraXOffest #already negative