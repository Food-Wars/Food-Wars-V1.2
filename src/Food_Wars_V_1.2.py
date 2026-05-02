# -*- coding: utf-8 -*-

#import standard libraries
from enum import Enum

#import 3rd party libraries
import pygame as pygame  #using pygame-ce

#import scripts
import scripts.data as data
import scripts.eventHandlers as handelers
import scripts.ecs as ecs

#initalise modules
pygame.init()
ecs.init()

#has to be after display.set_mode() so images can be conveted for performance
data.loadImages()
data.loadIcon()

#define states
class States(Enum):
    GAME = 0
    MENU = 1

#define game variables
fps = 64
clock = pygame.time.Clock()
gameState = States.GAME

dt = clock.tick(fps)

run = True
while run == True:

    dt /= 1000.0 #convert milliseconds to seconds

    data.screen.fill((0, 0, 0))
    #event handeler
    match gameState:
        case States.GAME:
            run = handelers.gameHandeler(dt)
        #fall back event handeler
        case _:
            for event in pygame.event.get():
                #handle_music(event, playlist, music)
                if event.type == pygame.QUIT:
                    run = False #if press x, end game loop
    #refresh the screen
    pygame.display.update() 
    #limit fps
    dt = clock.tick(fps)

#close window
pygame.quit()