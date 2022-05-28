import pygame
import random
import time
from PIL import Image
from GameLocations import GameLocations
from CaveObject import Cave
from Player import Player
from LazyWumpusObject import LazyWumpus
from Trivia import Trivia
from HighScoresObject import HighScores
from Sound import Sound


from pygame.locals import *

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
WHITE = (250, 250, 250)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

isContinued = False
Background = pygame.image.load(r'Images\MainScreen.png')
Background = pygame.transform.scale(Background, (1280, 720))

Caution = pygame.image.load(r'Images\Caution.png')
Caution = pygame.transform.scale(Caution, (52, 56))

Coin = pygame.image.load(r'Images\Koala.jpg')
Coin = pygame.transform.scale(Coin, (50, 50))




font = pygame.font.SysFont(None, 32)

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


background = BLACK


player = Player()
print("Player initialized")

wumpus = LazyWumpus()
print("Wumpus initialized")

cave = Cave()
print("Cave initialized")

location = GameLocations()
print("Location initialized")
# location.spawnItems(wumpus, cave, player)

trivia = Trivia()
print("Trivia initialized")

highScores = HighScores()
print("Highscores initialized")

sound = Sound(True)
print("Sound initialized")

print("Game initialized")



displayImg = font.render("It begins in a deeeeep dark cavern", True, WHITE)
displayImg2 = font.render("'Enter' to continue . . .", True, WHITE)
# input("Press enter to begin! ")
# playerName = input("What's your name? ")
location.spawnItemsRandom()
cave.loadPrevGame(r'MapFiles\demoFile.txt')
# for diagnostic purposes
print(location.getHazards())
# cave.printSelf()

class IO:

    connectionsText = 'this is the connections text'
    displayText = 'A dark a dusty room'
    displayText2 = 'this is the display text 2'
    inputText = 'input text'

    def drawFrame():

        displayImg = font.render(IO.displayText, True, WHITE)
        displayImg2 = font.render(IO.displayText2, True, WHITE)
        connectionsImg = font.render(IO.connectionsText, True, WHITE)
        inputImg = font.render(IO.inputText, True, WHITE)

        screen.fill(background)
        screen.blit(connectionsImg, displayRect3)
        screen.blit(inputImg, inputRect)
        screen.blit(displayImg, displayRect)
        screen.blit(displayImg2, displayRect2)

        inputRect.size=inputImg.get_size()
        cursor.topleft = inputRect.topright

        if time.time() % 1 > 0.5:
            pygame.draw.rect(screen, WHITE, cursor)
        pygame.display.update()

    def getInput(question):

        IO.playerInput = ""
        answered = False
        IO.displayText2 = question
        IO.inputText = ""
        IO.connectionsText = connections

        IO.drawFrame()

        while not answered:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                    exit()

                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        
                        IO.playerInput = IO.inputText
                        IO.inputText = ""
                        return IO.playerInput
                        
                    
                    if event.key == K_BACKSPACE:
                        if len(IO.inputText)>0:
                            IO.inputText = IO.inputText[:-1]
                    elif event.key != K_RETURN:
                        IO.inputText += event.unicode

            IO.drawFrame()      



def Move():

    based = False

    IO.displayText = "You choose a path to go down"
    IO.drawFrame()

    while not based:

        move = IO.getInput("Where to move?")

        if int(move) in cave.getConnections(player.pos):
            player.pos = int(move)
            sound.playSound("coin")
            print("Moved into", move)
            based = True
        
        else:
            move = IO.getInput("Not a valid response. Enter the number room you want to enter.")

def ShootArrow():

    based = False

    IO.displayText = "You choose a path shoot an arrow at"
    IO.drawFrame()

    while not based:

        direction = IO.getInput("Where to shoot?")

        if int(direction) in cave.getConnections(player.pos):
            sound.playSound("shoot")

            print("Shot at ", direction)
            based = True

            if location.shootArrow(int(direction), wumpus, cave, player):

                IO.displayText = "YOU KILLED THE WUMPUS"
                IO.drawFrame
                sound.playSound("arrHit")
                wumpus.changeToDead()

                print("hit wumpus")

            else:
                
                IO.displayText = "You missed"

                print("missed")
                #wumpus.changeToAwake()  this is done in GameLocations.shootArrow
            if player.arrows == 0:
                
                IO.displayText = "wumpus heard you and killed you"
        
        else:
            direction = IO.getInput("Not a valid response. Enter the number room you want to enter.")


turnNum = True
gameOn = True
# Our game loop
while gameOn:

    connections = str(cave.getConnections(player.pos))
    hazards = location.checkHazards(player.pos, wumpus, cave, player)

    turnType = IO.getInput("move OR shoot OR buy arrow")

    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False

        if event.type == KEYDOWN:

            # If the Backspace key has been pressed set
            # running to false to exit the main loop
            if event.key == K_ESCAPE:
                gameOn = False



    # if hazards == "W":
    #     # fight the wumpus
    #     FightWumpus()
    #     if not gameOn:
    #         # don't do the rest of the turn if you're dead
    #         break
    
    # if hazards == "B":
    #     GetMovedByBat()
    #     # moving is taken care of in GameLocations
    #     # continue to count this as a full turn, so hazards and warnings
    #     # are checked before player move/shoot
    #     continue
    # if hazards == "P":
    #     # moving to cavern 0 is done in GameLocations
    #     FallIntoPit()
    #     if not gameOn:
    #         break
    # if hazards == "WB":
    #     wumpus.changeToAwake()
    #     wumpus.moveWumpus(cave)
    #     print("you glimpse the wumpus")
    #     GetMovedByBat()
    #     continue
    # if hazards == "WP":
    #     print("you glimpse the wumpus")
    #     FallIntoPit()
    #     if not gameOn:
    #         break
    #     wumpus.changeToAwake()
    #     wumpus.moveWumpus(cave)

    # print("Player position:", player.pos)
    # print("Cave connections:", cave.getConnections(player.pos))
    # warnings = location.getWarnings(wumpus, cave, player)
    # if "PIT" in warnings:
    #     print("You feel a draft")
    #     sound.playSound("pit")
    # if "BAT" in warnings:
    #     print("You hear large wings flapping")
    #     sound.playSound("bat1")
    # if "WUMPUS" in warnings:
    #     print("You smell a wumpus")
    

    if turnType == "shoot":  
        ShootArrow()

    if turnType == "move":  
        Move()

    # elif answer == "buy arrow":
    #     BuyArrow()


    IO.drawFrame()
    turnNum += 1