# -*- coding: utf-8 -*-

#import 3rd party libraries
import pygame as pygame  #using pygame-ce

#import scripts
import scripts.data as data
import scripts.eventHandlers as handelers

#initalise modules
pygame.init()

#has to be after display.set_mode() so images can be conveted for performance
data.loadImages()
data.loadIcon()

#define game variables
fps = 60
clock = pygame.time.Clock()
gameState = "menu"

dt = clock.tick(fps)

run = True
while run == True:

    dt /= 1000.0 #convert milliseconds to seconds

    data.screen.fill((0, 0, 0))
    #event handeler
    match gameState:
        case "menu":
            run = handelers.menuHandeler(dt)
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