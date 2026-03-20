'''Stores all the event loops for different game states'''
#import 3rd party librareis
import pygame
import esper

#import scripts
from . import data
from . import renderers

def gameHandeler(dt):

    movement =  [False, False, False, False]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False #if press x, end game loop

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        movement[0] = True
    if keys[pygame.K_a]:
        movement[1] = True
    if keys[pygame.K_s]:
        movement[2] = True
    if keys[pygame.K_d]:
        movement[3] = True
    data.move(movement)


    renderers.renderMap()
    esper.process(dt)
    
    return True