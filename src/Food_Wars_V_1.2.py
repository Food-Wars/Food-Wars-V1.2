# -*- coding: utf-8 -*-

#import 3rd party libraries
import pygame as pygame  #using pygame-ce

#import scripts
import scripts.data as data

#initalise modules
pygame.init()


#load images
icon = pygame.image.load("game_files\imgs\gui\cupcake_icon.png")

#define screen
screen_height = 600
screen_width = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Food Wars")
pygame.display.set_icon(icon)

#has to be after display.set_mode() so images can be conveted for performance
data.loadImages()

#define game variables
fps = 60
clock = pygame.time.Clock()

run = True
while run == True:
    #event handeler
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