# -*- coding: utf-8 -*-

#import 3rd party libraries
import pygame as pygame  #using pygame-ce

#import scripts
import scripts.data as data
import scripts.eventHandlers as handelers

#initalise modules
pygame.init()

#load early for display setup
data.loadIcon()

#define screen
screen_height = 600
screen_width = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Food Wars")
pygame.display.set_icon(data.icon)

#has to be after display.set_mode() so images can be conveted for performance
data.loadImages()

#define game variables
fps = 60
clock = pygame.time.Clock()
gameState = "menu"

run = True
while run == True:
    screen.fill((0, 0, 0))
    #event handeler
    match gameState:
        case "menu":
            run = handelers.menuHandeler(screen)
        #fall back event handeler
        case _:
            for event in pygame.event.get():
                #handle_music(event, playlist, music)
                if event.type == pygame.QUIT:
                    run = False #if press x, end game loop
    #refresh the screen
    pygame.display.update() 
    #limit fps
    clock.tick(fps)

#close window
pygame.quit()