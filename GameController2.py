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


displayText = 'this is the display text'
inputText = ''

answer = inputText

font = pygame.font.SysFont(None, 32)

displayImg = font.render(displayText, True, WHITE)
displayImg2 = font.render(displayText, True, WHITE)
connectionsImg = font.render(displayText, True, WHITE)
inputImg = font.render(inputText, True, WHITE)


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
<<<<<<< Updated upstream
location.spawnItemsRandom()
=======
# location.spawnItemsRandom()
location.spawnItemsCustom(wumpus)
>>>>>>> Stashed changes
cave.loadPrevGame(r'MapFiles\demoFile.txt')
# for diagnostic purposes
print(location.getHazards())
# cave.printSelf()


def drawFrame():
    screen.fill(background)
    screen.blit(connectionsImg, displayRect3)
    screen.blit(inputImg, inputRect)
    screen.blit(displayImg, displayRect)
    screen.blit(displayImg2, displayRect2)
    if time.time() % 1 > 0.5:
        pygame.draw.rect(screen, WHITE, cursor)
    pygame.display.update()

def PlayerMove():

    based = False

    displayImg = font.render(hazardMessage, True, WHITE)
    screen.blit(displayImg, displayRect)
    pygame.display.update()

    while not based:
        move = getInput("Which way to go next????")
        if int(move) in cave.getConnections(player.pos):
            player.pos = int(move)
            sound.playSound("coin")
            print("Moved into", move)
            based = True
        
        else:
            move = getInput("Not a valid response. Enter the number room you want to enter.")
    
def ShootArrow():
    global gameOn


    
    direction = getInput("which room to shoot arrow at????")
    sound.playSound("shoot")
    while int(direction) not in cave.getConnections(player.pos):
       direction = getInput("Not a valid response. Enter the number room you want to shoot into.")
       sound.playSound("shoot")
    if location.shootArrow(int(direction), wumpus, cave, player):

        displayImg = font.render("YOU KILLED THE WUMPUS!!", True, WHITE)
        screen.blit(displayImg, displayRect)
        pygame.display.update()
        sound.playSound("arrHit")
        wumpus.changeToDead()

        print("hit something")

        gameOn = False
    else:
        displayImg = font.render("You missed :(", True, WHITE)
        screen.blit(displayImg, displayRect)
        pygame.display.update()

        print("missed")
        #wumpus.changeToAwake()  this is done in GameLocations.shootArrow
    if player.arrows == 0:
        displayImg = font.render("The Wumpus senses you're out of arrows and eats u lmaooo", True, WHITE)
        screen.blit(displayImg, displayRect)
        pygame.display.update()

        gameOn = False

        print("out of arrows")

def FightWumpus():
    global gameOn
    print("the wumpus is here. Fight for your life")
    sound.playSound("wumpus3")
    if trivia.challenge(3, 5, player):
        print("you escape the wumpus and move to a random connected room")
        player.pos = random.choice(cave.getConnections(player.pos))
        wumpus.changeToAwake()
        wumpus.moveWumpus(cave)
    else:
        print("the wumpus eats you")
        sound.playSound("plHit")
        gameOn = False

def BuyArrow():
    print("you attempt to purchase an arrow")
    if trivia.challenge(2, 3, player):
        player.arrows += 1
        print("gained one arrow")
        sound.playSound("coin")
    else:
        print("failed to get an arrow")

def BuySecret():
    print("you attempt to purchase a secret")
    if trivia.challenge(2, 3, player):
        player.arrows += 1
        print("here is your secret:")
        print(trivia.getSecret())
    else:
        print("failed to get a secret")

def GetMovedByBat():
    print("a bat sweeps you away")
    sound.playSound("bat2")
    player.pos = random.randint(0, 29)

def FallIntoPit():
    global gameOn
    print("you step into a pit. you attempt to catch yourself")
    if trivia.challenge(2, 3, player):
        print("you pull yourself out of the pit and find yourself in room 0")
    else:
        gameOn = False
        print("you plunge into darkness. game over")
        sound.playSound("amb1")

def getInput(question):
    inputText = ""
    inputImg = font.render(inputText, True, WHITE)
    displayImg2 = font.render(question, True, WHITE)

    playerInput = ""
    playerAnswered = False


    while not playerAnswered:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                exit()

            if event.type == KEYDOWN:

                if event.key == K_RETURN:
                    
                    playerInput = inputText
                    inputText = ""

                    playerAnswered = True
                    
                
                if event.key == K_BACKSPACE:
                    if len(inputText)>0:
                        inputText = inputText[:-1]
                elif event.key != K_RETURN:
                    inputText += event.unicode

                inputImg = font.render(inputText, True, WHITE)
                
                inputRect.size=inputImg.get_size()
                cursor.topleft = inputRect.topright

        

        

        if "WUMPUS" in location.getWarnings(wumpus, cave, player):
            screen.blit(Caution, (900, 550))

        #Coin manager
        if(player.coins > 0):
            screen.blit(Coin, (50, 50))

            if(player.coins > 1):
                screen.blit(Coin, (120, 50))

                if(player.coins > 2):
                    screen.blit(Coin, (190, 50))

        # screen.fill(background)
        hazardMessage = str(cave.getConnections(player.pos))
        connectionsImg = font.render(hazardMessage, True, WHITE)
        # screen.blit(connectionsImg, displayRect3)
        

        # screen.blit(inputImg, inputRect)
        # screen.blit(displayImg, displayRect)
        # screen.blit(displayImg2, displayRect2)
        # if time.time() % 1 > 0.5:
        #     pygame.draw.rect(screen, WHITE, cursor)
        # pygame.display.update()

        drawFrame()

    return playerInput

while isContinued == False:
    screen.blit(Background, (0, 0))



        
    for event in pygame.event.get() :
  

        if event.type == pygame.QUIT :
  
            pygame.quit()

            quit()

        if event.type == KEYDOWN:
            if event.key == K_RETURN : 

                print("Game Started")
                isContinued = True
                # Draws the surface object to the screen.  
        
    pygame.display.update() 



turnNum = 0
# Variable to keep our game loop run
gameOn = True
# Our game loop
while gameOn:
    # one turn per loop
    screen.fill(background)
    screen.blit(Caution, (900, 550))


    for event in pygame.event.get():
        if event.type == QUIT:
            gameOn = False

        if event.type == KEYDOWN:

            # If the Backspace key has been pressed set
            # running to false to exit the main loop
            if event.key == K_ESCAPE:
                gameOn = False



    # wumpAnswer = getInput("wump?????")
    # print(wumpAnswer)
    hazardMessage = str(cave.getConnections(player.pos))
    hazards = location.checkHazards(player.pos, wumpus, cave, player)

    #displayImg = font.render(hazardMessage, True, WHITE)

    answer = getInput("move OR shoot OR buy arrow")




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
        FallIntoPit()
        if not gameOn:
            break
    if hazards == "WB":
        wumpus.changeToAwake()
        wumpus.moveWumpus(cave)
        print("you glimpse the wumpus")
        GetMovedByBat()
        continue
    if hazards == "WP":
        print("you glimpse the wumpus")
        FallIntoPit()
        if not gameOn:
            break
        wumpus.changeToAwake()
        wumpus.moveWumpus(cave)

    print("Player position:", player.pos)
    print("Cave connections:", cave.getConnections(player.pos))
    warnings = location.getWarnings(wumpus, cave, player)
    if "PIT" in warnings:
        print("You feel a draft")
        sound.playSound("pit")
    if "BAT" in warnings:
        print("You hear large wings flapping")
        sound.playSound("bat1")
    if "WUMPUS" in warnings:
        print("You smell a wumpus")
    



    # actionChoice = input("shoot or move or buy arrow?")
    displayImg2 = displayImg2 = font.render("'shoot OR move OR buy arrow", True, WHITE)
    

    if answer == "shoot":  
        ShootArrow()

    elif answer == "move":  
        PlayerMove()

    elif answer == "buy arrow":
        BuyArrow()

    

    screen.blit(inputImg, inputRect)
    screen.blit(displayImg, displayRect)
    screen.blit(displayImg2, displayRect2)

    if time.time() % 1 > 0.5:
        pygame.draw.rect(screen, WHITE, cursor)
    pygame.display.update()

    turnNum += 1



try:
    highScores.addHighScore(playerName, player.computeEndScore(wumpus.getWumpState(), turnNum))
    print(highScores.getHighScores())
except:
    print("gameOn is false. error involving high score (line 36, in addHighScore)")




# class IO:


        