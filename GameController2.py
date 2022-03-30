import pygame
import random
from PIL import Image
from GameLocations import GameLocations
from cave import Cave
from Player import Player
from LazyWumpusObject import LazyWumpus
from Trivia import Trivia
from HighScoresObject import HighScores


from pygame.locals import *

# pygame.init()
# screen = pygame.display.set_mode((800, 600))

# background = pygame.image.load('images/Koala.jpg')


# def drawBackground():
#     screen.blit(background, (0, 0))


# drawBackground()


player = Player()

wumpus = LazyWumpus()

cave = Cave()

location = GameLocations()
# location.spawnItems(wumpus, cave, player)

trivia = Trivia()

highScores = HighScores()


print("game initialized")


# turnNum = 0
# # Variable to keep our game loop runngameOn = True
# gameOn = True
# # Our game loop
# while gameOn:

#     # FPS (in ms delay)
#     pygame.time.delay(20)


#     # for loop through the event queue
#     for event in pygame.event.get():

#         # Check for KEYDOWN event
#         if event.type == KEYDOWN:

#             # If the Backspace key has been pressed set
#             # running to false to exit the main loop
#             if event.key == K_ESCAPE:
#                 gameOn = False

#         # Check for QUIT event
#         elif event.type == QUIT:
#             gameOn = False

#         if event.type == pygame.MOUSEBUTTONDOWN:
#             print("clickkk")

#     pygame.display.update()

#     turnNum += 1

print("Welcome to Hunt the Wumpus!")
input("Press enter to begin! ")
playerName = input("What's your name? ")
location.spawnItems(wumpus, cave, player)
cave.genNewMap(location.getHazards())
# for diagnostic purposes
print(location.getHazards())
# cave.printSelf()

def PlayerMove():

    # based = False

    # while not based:
    #     move = input("Which way to go next????")
    #     if int(move) in cave.getConnections(player.pos):
    #         player.pos = int(move)
    #         print("based")
    #         based = True
    move = input("Where do you want to move?")
    while int(move) not in cave.getConnections(player.pos):
       move = input("Not a valid response. Enter the number room you want to enter.")
    player.pos = int(move)
    # you get a coin when you move
    player.coins += 1
    print("you moved")

def ShootArrow():
    global gameOn
    direction = input("which room to shoot arrow at????")
    while int(direction) not in cave.getConnections(player.pos):
       direction = input("Not a valid response. Enter the number room you want to shoot into.")
    if location.shootArrow(int(direction), wumpus, cave, player):
        print("you killed the wumpus!")
        wumpus.changeToDead()
        gameOn = False
    else:
        print("missed arrow")
        wumpus.changeToAwake()
    if player.arrows == 0:
        print("wumpus senses that you're out of arrows and eats you")
        gameOn = False

def FightWumpus():
    global gameOn
    print("the wumpus is here. Fight for your life")
    if trivia.challenge(3, 5, player):
        print("you escape the wumpus and move to a random connected room")
        player.pos = random.choice(cave.getConnections(player.pos))
        # need to wake wumpus up
    else:
        print("the wumpus eats you")
        gameOn = False

def BuyArrow():
    print("you attempt to purchase an arrow")
    if trivia.challenge(2, 3, player):
        player.arrows += 1
        print("gained one arrow")
    else:
        print("failed to get an arrow")


turnNum = 0
# Variable to keep our game loop run
gameOn = True
# Our game loop
while gameOn:
    # one turn per loop
    hazards = location.checkHazards(player.pos, wumpus, cave, player)
    print("\nHazards:", hazards)
    if hazards == "W":
        # fight the wumpus
        FightWumpus()
        if not gameOn:
            # don't do the rest of the turn if you're dead
            break

    print("Player position:", player.pos)
    print("Cave connections:", cave.getConnections(player.pos))
    print("Warnings:", location.getWarnings(wumpus, cave, player))

    actionChoice = input("shoot or move or buy arrow?")
    if actionChoice == "shoot":
        ShootArrow()
    elif actionChoice == "move":   
        PlayerMove()
    elif actionChoice == "buy arrow":
        BuyArrow()

    turnNum += 1

try:
    highScores.addHighScore(playerName, player.computeEndScore(wumpus.getWumpState(), turnNum))
    print(highScores.getHighScores())
except:
    print("gameOn is false. error involving high score (line 36, in addHighScore)")