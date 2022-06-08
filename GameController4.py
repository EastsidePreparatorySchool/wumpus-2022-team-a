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
# cave.loadPrevGame(r'MapFiles\demoFile.txt')
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
            if player.coinsAll < 100:
                player.coinsAll += 1
                player.coinsNow += 1
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
    IO.write("You attempt to purchase an arrow.")
    if trivia.challenge(2, 3):
        player.arrows += 1
        IO.write("Gained one arrow!")
        sound.playSound("coin")
    else:
        IO.write("Failed to buy an arrow.")

def BuySecret():
    IO.write("You attempt to purchase a secret.")
    if trivia.challenge(2, 3):
        player.arrows += 1
        IO.write("Here is your secret: ", trivia.getSecret())
        IO.getInput()
        # clear secret from display
        IO.write(" ")
    else:
        IO.write("Failed to get a secret.")

# define interactions with wumpus or hazards

def FightWumpus():
    global gameOn
    IO.write("The wumpus is here. Fight for your life.")
    #IO.getInput("Press Enter to begin the fight.")
    sound.playSound("wumpus3")
    if trivia.challenge(3, 5):
        IO.write("You escape the wumpus and move to a random connected room.")
        wumpus.setTurnsToMove(wumpus.trivia())
        wumpus.changeToAwake()
        player.pos = random.choice(cave.getConnections(player.pos))
        
    else:
        IO.write("", "The wumpus eats you.")
        sound.playSound("plHit")
        gameOn = False

def GetMovedByBat():
    #IO.write("A bat sweeps you away")
    IO.write("Claws grip your neck and hoist you upward.")
    IO.getInput()
    IO.write("Airborne, you careen through the cave, nearly colliding with its guano-covered walls.")
    sound.playSound("bat2")
    IO.getInput()
    IO.write("The bat drops you in room " + str(player.pos) + ".")
    IO.getInput()
    # clear display text
    IO.write(" ")
    player.pos = random.randint(0, 29)

# returns true if you died, false if survived
def FallIntoPit():
    IO.write("You stumble as the ground becomes the top of a cliff. You try to catch yourself!")
    if trivia.challenge(2, 3):
        IO.write("You pull yourself out of the pit and recognize this as the room you began in.")
        return False
    else:
        #IO.write("", "You plunge into darkness. game over")
        IO.write("You fall toward the center of the pit.")
        IO.getInput()
        IO.write("You feel your feet slip away from the last vestige of solid rock.")
        IO.getInput()
        sound.playSound("amb1")
        coinMessage = "You feel nothing but the "
        if player.coinsNow > 1:
            coinMessage += "weight of gold in your pocket "
        elif player.coinsNow == 1:
            coinMessage += "coolness of your last coin on your tense fingers "
        else:
            coinMessage += "emptiness of your pockets "
        coinMessage += "as you plunge into darkness. Game over."
        IO.write(coinMessage)
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

isContinued = False
loadPreset = False
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

                loadPreset = (IO.MenuePos%3 == 1)

                if IO.MenuePos%3 == 0 or IO.MenuePos%3 == 1:
                    print("game started")
                    isContinued = True

                if IO.MenuePos%3 == 2:
                    pygame.quit()
                    quit()

        
    IO.drawMenueFrame()



#displayImg = font.render("It begins in a deeeeep dark cavern", True, WHITE)
#displayImg2 = font.render("'Enter' to continue . . .", True, WHITE)
playerName = IO.getInput("Enter player name:")

if loadPreset:
    mapNum = IO.getInput("Enter preset map number:")
    cave.loadPresetMap(int(mapNum))
else:
    cave.genNewMap(location.getHazards())

IO.getInput("You find yourself in a deep, dark cavern. Press Enter to continue...")


turnNum = 0 
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

        # IMPORTANT!!!!
        # got rid of continues because wumpus behind the scene movement
        # must still happen
    if hazards == "P":
        # moving to cavern 0 is done in GameLocations
        if FallIntoPit():
            gameOn = False
            break
            # TODO probably only one of the above lines is necessary
    if hazards == "WB":
        wumpus.setTurnsToMove(1)
        wumpus.changeToAwake()
        IO.getInput("you glimpse the wumpus before...")
        GetMovedByBat()
    if hazards == "WP":
        wumpus.setTurnsToMove(1)
        wumpus.changeToAwake()
        IO.getInput("you glimpse the wumpus before...")
        if FallIntoPit():
            gameOn = False
            break
            # TODO probably only one of the above lines is necessary



    print(location.getWarnings())
    #IO.write("Player position:" + str(player.pos))
    #IO.write("Nearby rooms: " + str(cave.getConnections(player.pos)))  consolidating this message with the thing that always shows connected rooms
    warnings = location.getWarnings()
    if "PIT" in warnings:
        IO.write("You feel a draft")
        sound.playSound("pit")
    if "BAT" in warnings:
        IO.write("You hear large wings flapping")
        sound.playSound("bat1")
    if "WUMPUS" in warnings:
        IO.write("You smell a wumpus")
        sound.playSound(random.choice(("wumpus1", "wumpus2")))
    
    # player chooses which action to take
    turnType = IO.getInput("move OR shoot OR buy arrow OR buy secret", location.getWarnings())

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

    wumpus.endTurnMove(cave, turnNum)
    warnings = location.getWarnings()
    IO.drawFrame()
    turnNum += 1

IO.getInput()

# TODO tell player their score, note both displays might already be in use so maybe wait
# before doing this

print("game over")

score = player.computeEndScore(wumpus.getWumpState(), turnNum)
print("your score is " + str(score))
highScores.addHighScore("player1", score)
highScoresList = highScores.getHighScores()
highScores.addHighScore(playerName, score)
highScores.writeHighScores()

#NEED TO SEND THIS TO PYGAME WINDOW
print(highScoresList)

# keep window running until player closes it
while True:
    if not checkGameQuit():
        break