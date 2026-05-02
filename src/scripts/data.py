'''This is a file for storing global data from files'''

#import standard libraries
from pathlib import Path

#import 3rd party libraries
import pygame
import esper

#import scripts
from . import worldGen
from . import imgHandeler

#         Define Variables
#--------------------------------------

screen_height = 600
screen_width = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Food Wars")

#image data
icon = None
terrainSprites = None

#world datas
chunks = {}

#camara data
camaraChunk = [0, 0]
camaraXOffset = 0
camaraYOffset = 0

#         Define Functions
#--------------------------------------

def loadIcon():
    global icon
    icon = pygame.image.load(Path("game_files", "imgs", "icons", "cupcake_icon.png"))
    pygame.display.set_icon(icon)

def loadImages():
    global terrainSprites
    terrainSprites = imgHandeler.loadImgs(Path("game_files", "imgs", "tiles", "tiles.json"))
    terrainSprites["img"].convert() #reccomended for blit speed

def getChunk(x, y):
    if (x, y) in chunks.keys():
        return chunks[(x, y)]
    chunks[(x, y)] = worldGen.generateChunk(x, y)
    return chunks[(x, y)]

def getImg(imgSet, name):
    match imgSet():
        case "terrain":
            surf = terrainSprites["img"]
            coords = terrainSprites[name]["coords"]
        case _:
            surf = pygame.Surface((5, 5))
            surf.fill((0, 0, 0))
            coords = (0, 0, 5, 5)
    return surf, coords

def move(directions):
    global camaraChunk
    global camaraXOffset
    global camaraYOffset

    #directions storead as (w, a, s, d)
    distances = [0.0, 0.0]
    if directions[0]:
        distances[1] += 5
    elif directions[1]:
        distances[0] -= 5
    if directions[2]:
        distances[1] -= 5
    elif directions[3]:
        distances[0] += 5
    
    
    camaraChunk, camaraXOffset, camaraYOffset = getMovePositions(camaraChunk, camaraXOffset, camaraYOffset, distances)

def getMovePositions(chunk, xOffset, yOffset, distances):
    '''handles movement with chunk and offset system'''

    xOffset += distances[0]
    yOffset += distances[1]

    if yOffset > 128:
        chunk[1] -= 1
        yOffset = 0 + (yOffset - 128)
    elif camaraYOffset < 0:
        chunk[1] += 1
        yOffset = 128 + yOffset #already negative

    if xOffset > 128:
        chunk[0] += 1
        xOffset = 0 + (xOffset - 128)
    elif xOffset < 0:
        chunk[0] -= 1
        xOffset = 128 + xOffset #already negative
    
    return chunk, xOffset, yOffset
