# from lib2to3.pygram import python_grammar_no_print_statement

import pygame, keyboard, time
from pygame.locals import *

class GameControl:

    pygame.init()

    background_colour = (255,255,255)
    (width, height) = (800, 600)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Tutorial 1')
    screen.fill(background_colour)
    pygame.display.flip()
        

    keepGameRunning = True
    while keepGameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGameRunning = False

    while True:

        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    keepGameRunning = False
                    
                elif event.type == QUIT:
                    keepGameRunning = False

     