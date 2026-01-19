# -*- coding: utf-8 -*-

#import 3rd party libraries
#using pygame-ce
import pygame as pygame 

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