'''Stores all the event loops for different game states'''

import pygame

from . import data
from . import renderers

def menuHandeler(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False #if press x, end game loop
    #render background
    renderers.renderMap(screen)
    
    return True