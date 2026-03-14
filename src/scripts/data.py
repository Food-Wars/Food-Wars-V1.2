'''This is a file for storing global data from files'''

import os

import pygame

terrainSprites = None

def loadImages():
    global terrainSprites
    terrainSprites = pygame.image.load(os.path.join("game_files", "imgs", "tiles", "tiles_background.png"))
    terrainSprites.convert() #reccomended for blit speed