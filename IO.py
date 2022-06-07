import pygame
from pygame.locals import * # do we need to import all of these?
import MainObjects
import time

# note: pygame docs say it is safe to call pygame.init() multiple times
pygame.init()

WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
loc1 = (480, 450)
loc2 = (480, 500)
loc3 = (480, 550)
MenuePos = 0
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
MenueBackground = pygame.image.load(r'Images\MainScreen.png')
MenueBackground = pygame.transform.scale(MenueBackground, (1280, 720))
Cursor = pygame.image.load(r'Images\Cursor.png')
Cursor = pygame.transform.scale(Cursor, (40, 30))
Coin = pygame.image.load(r'Images\Koala.jpg')
Coin = pygame.transform.scale(Coin, (50, 50))
font = pygame.font.SysFont(None, 32)
background = BLACK
player = MainObjects.player
cave = MainObjects.cave

connectionsText = ""
displayText = ""
displayText2 = ""
inputText = ""


def drawMenueFrame():

    screen.blit(MenueBackground, (0,0))

    if MenuePos%3 is 0:
        screen.blit(Cursor, loc1 )
    if MenuePos%3 is 1:
        screen.blit(Cursor, loc2 )
    if MenuePos%3 is 2:
        screen.blit(Cursor, loc3)
    
    pygame.display.update() 



def drawFrame():

    displayImg = font.render(displayText, True, WHITE)
    displayImg2 = font.render(displayText2, True, WHITE)
    connectionsImg = font.render(connectionsText, True, WHITE)
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

    screen.fill(background)
    screen.blit(connectionsImg, displayRect3)
    screen.blit(inputImg, inputRect)
    screen.blit(displayImg, displayRect)
    screen.blit(displayImg2, displayRect2)

    #Coin manager
    if(player.coins > 0):
        screen.blit(Coin, (50, 50))

        if(player.coins > 1):
            screen.blit(Coin, (120, 50))

            if(player.coins > 2):
                screen.blit(Coin, (190, 50))

    inputRect.size=inputImg.get_size()
    cursor.topleft = inputRect.topright

    if time.time() % 1 > 0.5:
        pygame.draw.rect(screen, WHITE, cursor)
    pygame.display.update()

# prompt user for text input
def getInput(question):
    global displayText2
    global connectionsText
    global inputText

    playerInput = ""
    answered = False
    displayText2 = question
    inputText = ""
    connectionsText = str(cave.getConnections(player.pos))

    drawFrame()

    while not answered:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    playerInput = inputText
                    inputText = ""
                    return playerInput
                elif event.key == K_BACKSPACE:
                    if len(inputText)>0:
                        inputText = inputText[:-1]
                else:
                    inputText += event.unicode

        drawFrame()

# displays a two-line message on the game screen
def write(messageLine1, messageLine2=""):
    global displayText
    global displayText2
    if messageLine1 != "":
        # if you have an empty string for first parameter, then the previous first-line output will
        # remain on screen
        displayText = str(messageLine1)
    displayText2 = str(messageLine2)
    drawFrame()