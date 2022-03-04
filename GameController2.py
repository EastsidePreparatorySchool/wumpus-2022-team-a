import pygame
from PIL import Image
from GameLocations import GameLocations
from cave import Cave
from Player import Player
from LazyWumpusObject import LazyWumpus


from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('images/Koala.jpg')


def drawBackground():
    screen.blit(background, (0, 0))


drawBackground()


player = Player()

wumpus = LazyWumpus()

cave = Cave()

location = GameLocations()

location.spawnItems(wumpus, cave, player)





turnNum = 0
# Variable to keep our game loop runngameOn = True
gameOn = True
# Our game loop
while gameOn:

    # FPS (in ms delay)
    pygame.time.delay(20)


    # for loop through the event queue
    for event in pygame.event.get():

        # Check for KEYDOWN event
        if event.type == KEYDOWN:

            # If the Backspace key has been pressed set
            # running to false to exit the main loop
            if event.key == K_ESCAPE:
                gameOn = False

        # Check for QUIT event
        elif event.type == QUIT:
            gameOn = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("clickkk")

    pygame.display.update()


    turnNum += 1