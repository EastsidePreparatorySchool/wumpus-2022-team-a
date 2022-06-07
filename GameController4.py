import pygame
from pygame.locals import *
import random
import time
from PIL import Image
import IO
# from GameLocations import GameLocations
# from CaveObject import Cave
# from Player import Player
# from LazyWumpusObject import LazyWumpus
# from Trivia import Trivia
# from HighScoresObject import HighScores
# from Sound import Sound
import MainObjects

# copy the main objects for easier use
location = MainObjects.location
cave = MainObjects.cave
player = MainObjects.player
wumpus = MainObjects.wumpus
trivia = MainObjects.trivia
highScores = MainObjects.highScores
sound = MainObjects.sound

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
WHITE = (250, 250, 250)

pygame.init()
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  this and some related variables have been moved to IO

isContinued = False
Background = pygame.image.load(r'Images\MainScreen.png')
Background = pygame.transform.scale(Background, (1280, 720))

Caution = pygame.image.load(r'Images\Caution.png')
Caution = pygame.transform.scale(Caution, (52, 56))

# Coin = pygame.image.load(r'Images\Koala.jpg')
# Coin = pygame.transform.scale(Coin, (50, 50))




font = IO.font

displayImg = font.render("displayText", True, WHITE)
displayImg2 = font.render("displayText2", True, WHITE)
connectionsImg = font.render("connectionsText", True, WHITE)
inputImg = font.render("inputText", True, WHITE)


displayRect = displayImg.get_rect()
displayRect2 = displayImg.get_rect()
displayRect3 = displayImg.get_rect()
displayRect.topleft = (20, 420)
displayRect2.topleft = (20, 450)
displayRect3.topleft = (20, 390)

inputRect = inputImg.get_rect()
inputRect.topleft = (20, 530)
cursor = Rect(inputRect.topright, (3, inputRect.height))


# background = BLACK


print("Game initialized")





# input("Press enter to begin! ")
# playerName = input("What's your name? ")
# location.spawnItemsRandom()
location.spawnItemsCustom(wumpus, 11) # Spawn wumpus at 5
cave.loadPrevGame(r'MapFiles\demoFile.txt')
# for diagnostic purposes
print(location.getHazards())
# cave.printSelf()

# define player options

def Move():

    based = False

    IO.write("You choose a path to go down")

    while not based:

        move = IO.getInput("Where to move?")

        if int(move) in cave.getConnections(player.pos):
            player.pos = int(move)
            player.coins += 1
            sound.playSound("coin")
            IO.write("Moved into " + move)
            based = True

        else:
            move = IO.getInput("Not a valid response. Enter the number room you want to enter.")

def ShootArrow():

    based = False

    IO.write("You choose a room to shoot an arrow into")

    while not based:

        direction = IO.getInput("Where to shoot?")

        if int(direction) in cave.getConnections(player.pos):
            sound.playSound("shoot")

            IO.write("Shot at " + direction)
            based = True

            if location.shootArrow(int(direction), wumpus, cave, player):

                IO.write("YOU KILLED THE WUMPUS")
                sound.playSound("arrHit")
                wumpus.changeToDead()

            else:
                
                IO.write("You missed")
                #wumpus.changeToAwake()  this is done in GameLocations.shootArrow
            if player.arrows == 0:
                
                IO.write("wumpus senses that you have no arrows left, and it kills you")
        
        else:
            direction = IO.getInput("Not a valid response. Enter the number room you want to enter.")

def BuyArrow():
    if trivia.challenge(2, 3):
        player.arrows += 1
        IO.write("gained one arrow")
        sound.playSound("coin")
    else:
        IO.write("failed to buy an arrow")

def BuySecret():
    IO.write("you attempt to purchase a secret")
    if trivia.challenge(2, 3):
        player.arrows += 1
        IO.write("here is your secret: " + trivia.getSecret())
    else:
        IO.write("failed to get a secret")

# define interactions with wumpus or hazards

def FightWumpus():
    global gameOn
    IO.write("the wumpus is here. Fight for your life.")
    IO.getInput("Press Enter to begin the fight.")
    sound.playSound("wumpus3")
    if trivia.challenge(3, 5):
        IO.write("you escape the wumpus and move to a random connected room")
        player.pos = random.choice(cave.getConnections(player.pos))
        wumpus.changeToAwake()
        wumpus.moveWumpus(cave)
    else:
        IO.write("", "the wumpus eats you")
        sound.playSound("plHit")
        gameOn = False

def GetMovedByBat():
    IO.write("a bat sweeps you away")
    sound.playSound("bat2")
    player.pos = random.randint(0, 29)

# returns true if you died, false if survived
def FallIntoPit():
    IO.write("you step into a pit. you attempt to catch yourself")
    if trivia.challenge(2, 3):
        IO.write("you pull yourself out of the pit and find yourself in room 0")
        return False
    else:
        IO.write("", "you plunge into darkness. game over")
        sound.playSound("amb1")
        return True


# check if player is closing game window -- return false if game is being quit
def checkGameQuit():
    global gameOn
    for event in pygame.event.get():
            if event.type == QUIT:
                return False

            if event.type == KEYDOWN:

                # If the Backspace key has been pressed set
                # running to false to exit the main loop
                if event.key == K_ESCAPE:
                    return False
    # true if they're not closing window
    return True

def giveWarnings():
    return location.getWarnings(wumpus, cave, player)

isContinued = False
while isContinued == False:


    for event in pygame.event.get() :
  

        if event.type == pygame.QUIT :
  
            pygame.quit()

            quit()

        if event.type == KEYDOWN:
            if event.key == K_UP : 

                IO.MenuePos -= 1
                # Draws the surface object to the screen.  
            if event.key == K_DOWN :

                IO.MenuePos += 1 
            
            if event.key == K_RETURN:

                if IO.MenuePos%3 == 0:

                    print("game started")

                    isContinued = True
                
                if IO.MenuePos%3 == 2:

                    pygame.quit()

                    quit()

        
    IO.drawMenueFrame()



#displayImg = font.render("It begins in a deeeeep dark cavern", True, WHITE)
#displayImg2 = font.render("'Enter' to continue . . .", True, WHITE)
IO.getInput("You find yourself in a deep, dark cavern. Press Enter to continue...")

turnNum = True # why is this a boolean instead of a number?
gameOn = True
# Our game loop
while gameOn:

    connections = str(cave.getConnections(player.pos))
    hazards = location.checkHazards(player.pos, wumpus, cave, player)
    gameOn = checkGameQuit()

    if hazards == "W":
        # fight the wumpus
        FightWumpus()
        if not gameOn:
            # don't do the rest of the turn if you're dead
            break
    
    if hazards == "B":
        GetMovedByBat()
        # moving is taken care of in GameLocations
        # continue to count this as a full turn, so hazards and warnings
        # are checked before player move/shoot
        continue
    if hazards == "P":
        # moving to cavern 0 is done in GameLocations
        if FallIntoPit():
            gameOn = False
            break
            # TODO probably only one of the above lines is necessary
    if hazards == "WB":
        wumpus.changeToAwake()
        wumpus.moveWumpus(cave)
        IO.getInput("you glimpse the wumpus before...")
        GetMovedByBat()
        continue
    if hazards == "WP":
        IO.getInput("you glimpse the wumpus before...")
        if FallIntoPit():
            gameOn = False
            break
            # TODO probably only one of the above lines is necessary
        wumpus.changeToAwake()
        wumpus.moveWumpus(cave)
    

    # this should probably be moved to after hazards are checked
    print(location.getWarnings(wumpus, cave, player))
    turnType = IO.getInput("move OR shoot OR buy arrow OR buy secret", location.getWarnings(wumpus, cave, player))

    #IO.write("Player position:" + str(player.pos))
    IO.write("Nearby rooms: " + str(cave.getConnections(player.pos)))
    warnings = location.getWarnings(wumpus, cave, player)
    if "PIT" in warnings:
        IO.write("You feel a draft")
        sound.playSound("pit")
    if "BAT" in warnings:
        IO.write("You hear large wings flapping")
        sound.playSound("bat1")
    if "WUMPUS" in warnings:
        IO.write("You smell a wumpus")
    

    if turnType == "shoot":  
        ShootArrow()
        if wumpus.wumpState == "DEAD":
            gameOn = False
    elif turnType == "move":  
        Move()
    elif turnType == "buy arrow":
        BuyArrow()
    elif turnType == "buy secret":
        BuySecret()

    warnings = location.getWarnings(wumpus, cave, player)
    IO.drawFrame()
    turnNum += 1

# TODO tell player their score, note both displays might already be in use so maybe wait
# before doing this

print("game over")
# keep window running until player closes it
while True:
    if not checkGameQuit():
        break