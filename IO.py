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
shownWarnings = []

MenueBackground = pygame.image.load(r'Images\MainScreen.png')
MenueBackground = pygame.transform.scale(MenueBackground, (1280, 720))

Cursor = pygame.image.load(r'Images\Cursor.png')
Cursor = pygame.transform.scale(Cursor, (40, 30))

Coin = pygame.image.load(r'Images\Coin.png')
Coin = pygame.transform.scale(Coin, (50, 50))

Arrow = pygame.image.load(r'Images\Arrow.png')
Arrow = pygame.transform.scale(Arrow, (50, 50))

Caution = pygame.image.load(r'Images\Caution.png')
Caution = pygame.transform.scale(Caution, (23, 24))

CautionUnlit = pygame.image.load(r'Images\CautionUnlit.png')
CautionUnlit = pygame.transform.scale(CautionUnlit, (23, 24))


font = pygame.font.SysFont(None, 32)

background = BLACK
player = MainObjects.player
cave = MainObjects.cave
sound = MainObjects.sound

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


# you can leave the warnings parameter blank if you want the displayed warnings to continue to
# be whatever you last set them to
def drawFrame(warnings=shownWarnings):
    displayImg = font.render(displayText, True, WHITE)
    displayImg2 = font.render(displayText2, True, WHITE)
    connectionsImg = font.render(connectionsText, True, WHITE)
    inputImg = font.render(inputText, True, WHITE)

    WumpusImg = font.render("Wumpus", True, WHITE)
    PitsImg = font.render("Pits", True, WHITE)
    BatsImg = font.render("Bats", True, WHITE)

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
    
    global shownWarnings
    shownWarnings = warnings

    if "WUMPUS" in warnings:
        screen.blit(Caution, (900, 500))
        screen.blit(WumpusImg, (950, 500))
    else:
        screen.blit(CautionUnlit, (900, 500))
        screen.blit(WumpusImg, (950, 500))
    if "PIT" in warnings:
        screen.blit(Caution, (900, 550))
        screen.blit(PitsImg, (950, 550))
    else:
        screen.blit(CautionUnlit, (900, 550))
        screen.blit(PitsImg, (950, 550))
    if "BAT" in warnings:
        screen.blit(Caution, (900, 600))
        screen.blit(BatsImg, (950, 600))
    else:
        screen.blit(CautionUnlit, (900, 600))
        screen.blit(BatsImg, (950, 600))
    
    

    

    for n in range(player.coinsNow):
        screen.blit(Coin, (60 + 70*n, 50))

    for n in range(player.arrows):
        screen.blit(Arrow, (1160 - 70*n, 50))

    inputRect.size=inputImg.get_size()
    cursor.topleft = inputRect.topright

    if time.time() % 1 > 0.5:
        pygame.draw.rect(screen, WHITE, cursor)
    pygame.display.update()

# prompt user for text input. question can be empty to keep previous display text
def getInput(question="", warnings=shownWarnings):

    global shownWarnings
    shownWarnings = warnings

    global displayText2
    global connectionsText
    global inputText

    playerInput = ""
    answered = False
    if question != "":
        displayText2 = question
    else:
        # add a space between sentences if necessary
        if len(displayText2) > 0 and displayText2[-1] != ' ':
            displayText2 += " "
        displayText2 += "'Enter' to continue..."
    inputText = ""
    connectionsText = "Nearby rooms: " + str(cave.getConnections(player.pos))

    drawFrame(warnings)

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

        drawFrame(warnings)

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