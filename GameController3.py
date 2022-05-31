import pygame
import random
import time
from PIL import Image
from GameLocations import GameLocations
from CaveObject import Cave
from Player import Player
from LazyWumpusObject import LazyWumpus
# from Trivia import Trivia
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

# trivia = Trivia()
# print("Trivia initialized")

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



class NewTrivia:
    UsedTrivia = []

    def __init__(self):
        self.newGame()
    

    def TriviaText():

        IO.displayText = "dfdskalfjdsklajfkldsa"
        IO.drawFrame()

    def newGame(self):
        # call at some point during the process of a game starting? might not be necessary
        # eventually UsedTrivia should be stored in a file when the game is closed (if there's a run in progress), and there should be a Trivia.loadGame() function that reads that file
        self.UsedTrivia = []
        knownSecrets = open("TriviaFiles/KnownSecrets.txt", "w")
        knownSecrets.write("")
        knownSecrets.close()

    def challenge(self, needCorrect, maxAttempts, player):
        # call when player action prompts a trivia battle (buying a secret, fighting the wumpus, buying arrows, etc.)
        # needCorrect and maxAttempts can be int or str
        # player is the object
        # returns True on success, False on failure (and 1 on death by bankruptcy?) (maybe change to 1, 0, 2?)
        IO.displayText = ("the player has " + str(maxAttempts) + " tries to get " + str(needCorrect) + " questions right")
        IO.drawFrame()

        correct = 0
        attempts = 0
        for i in range(int(maxAttempts)):
            if player.coins > 0:
                player.coins -= 1
            else:
                IO.displayText = ("no coins, can't answer trivia")
                IO.drawFrame()
                return False
            if (self.askQuestion()):
                correct += 1
            attempts += 1
            if (correct >= int(needCorrect)):
                return True
        return False

    def askQuestion(self):
        # used only by Trivia Object
        # right returns True, wrong returns False

        allTriviaFile = open("TriviaFiles/TriviaQA.txt", "r")
        allTrivia = allTriviaFile.readlines()
        allTriviaFile.close()

        questionNum = 0
        numUnusedTrivia = 0

        # count how many used and unused questions are in the QA file
        for line in allTrivia:
            if (line[0] != 'q'):
                continue
            if (self.UsedTrivia.count(questionNum) == 0):
                numUnusedTrivia += 1
            questionNum += 1
        
        if numUnusedTrivia == 0:
            IO.displayText = ("all trivia questions have been used")
            IO.drawFrame()

        # choose a random unused trivia question
        chosenQNum = random.randrange(0, numUnusedTrivia)
        
        list.sort(self.UsedTrivia)
        for usedQNum in self.UsedTrivia:
            if (usedQNum <= chosenQNum):
                chosenQNum += 1
        
        self.UsedTrivia.append(chosenQNum)
        question = allTrivia[chosenQNum * 2]
        questionText = question[2:] # what the player will be asked
        isWritten = (question[1] == 'w')
        answerLine = allTrivia[chosenQNum * 2 + 1][:-1] # line holding answers (includes all choices), does not include line break
        correctAnswers = []
        # written answer question
        if isWritten:
            correctAnswers = answerLine.split("|")
        # multiple choice question
        else:
            # make a list of the available choices, with the leading c or w
            choices = answerLine.split("|")
            random.shuffle(choices)
            questionText += "Choices:\n"
            for choice in choices:
                questionText += '\t' + choice[1:] + '\n'
                if choice[0] == 'c':
                    correctAnswers.append(choice[1:])
            choices = [choice[1:] for choice in choices] # remove leading c/w
        while True:
            playerAnswer = IO.getInput(questionText)
            if isWritten or playerAnswer in choices:
                break
            IO.displayText = (playerAnswer + " is invalid. Type one of the given choices.")
            IO.drawFrame()

        if str(playerAnswer).lower() in correctAnswers:
            IO.displayText = ("Correct!")
            IO.drawFrame()

            return True
        else:
            #print("Sorry! The correct answer was " + allTrivia[chosenQNum * 2 + 1][:-1] + ".")
            if len(correctAnswers) == 1:
                IO.displayText = ("Sorry! The correct answer was: " + correctAnswers[0])
                IO.drawFrame()
            else:
                message = "Sorry! The acceptible answers were: "
                for answer in correctAnswers:
                    message += "\n\t" + answer
                IO.displayText = (message)
                IO.drawFrame()

            return False
    
    # generate a message to send based on distance from player to a hazard/wumpus
    def getDistSecret(self, cave, locations, playerRoom, wumpRoom, type):
        if type == "wumpus":
            distance = cave.getDist(playerRoom, wumpRoom)
            return "The wumpus is " + str(distance) + " caverns away from you."
        elif type == "bat":
            allRooms = locations.getHazards()
            # get a list of two room numbers, which are the two that have a bat
            batRooms = [index for index in range(len(allRooms)) if allRooms[index] == "BAT"]
            # find which bat is closer to the player
            firstDistance = cave.getDist(playerRoom, batRooms[0])
            secondDistance = cave.getDist(playerRoom, batRooms[1])
            distance = min(firstDistance, secondDistance)
            return "The nearest super bat is " + str(distance) + " caverns away from you."
        elif type == "pit":
            allRooms = locations.getHazards()
            # get a list of two room numbers, which are the two that have a pit
            pitRooms = [index for index in range(len(allRooms)) if allRooms[index] == "PIT"]
            # find which pit is closer to the player
            firstDistance = cave.getDist(playerRoom, pitRooms[0])
            secondDistance = cave.getDist(playerRoom, pitRooms[1])
            distance = min(firstDistance, secondDistance)
            return "The nearest bottomless pit is " + str(distance) + " caverns away from you."

    def getSecret(self, locations, cave, playerRoom, wumpRoom):
        # call when player successfully buys a secret
        # pass gameLocations as argument
        # i think i'll need the cave to be passed so i can find how far away something is (in terms of how many turns it would take to get there) (this could be the same function as what's used for checking for warnings)
        # chooses a random secret from a file of secrets or from trivia answers
        # returns the secret as a string
        # adds the secret to a file of known secrets
        # secrets can be (1=common, 5=rare):
        #   (1) information about the location of a hazard or wumpus (how close it is to you, what the nearest wumpus/hazard is)
        #   (2) "lore" or information that will help solve trivia
        #   (3) a list of some trivia answers (without the question)
        #   (5) a partial map of the cave?
        # all of these next ones will be in terms of distance, not room number (they're arbitrary/incorrect room numbers now because it's easier, as a placeholder)
        if random.random() < 0.3:
            secret = self.getDistSecret(cave, locations, playerRoom, wumpRoom, "bat")
        elif random.random() < 0.5:
            secret = self.getDistSecret(cave, locations, playerRoom, wumpRoom, "pit")
        elif random.random() < 0.7:
            secret = self.getDistSecret(cave, locations, playerRoom, wumpRoom, "wumpus")
        else:
            secret = "The wumpus likes warm colors"
        knownSecrets = open("TriviaFiles/KnownSecrets.txt", "a")
        # next line should be modified so you don't have an extra \n at end of file, maybe
        knownSecrets.write(secret + "\n")
        knownSecrets.close()
        return secret
    
    def getKnownSecrets(self):
        # returns all known secrets from a file, as an array of strings
        # intention: player can look at a notebook to see all the secrets they've gleaned (maybe should include trivia they've been asked)
        knownSecrets = open("TriviaFiles/KnownSecrets.txt", "r")
        secrets = knownSecrets.read()
        knownSecrets.close()
        # remove the trailing \n
        secrets = secrets[:-1]
        return secrets
   


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

def BuyArrow():
    if NewTrivia.challenge(2, 3, player):
        player.arrows += 1
        IO.displayText = ("gained one arrow")
        IO.drawFrame()
        sound.playSound("coin")
    else:
        IO.displayText = ("failed to buy an arrow")
        IO.drawFrame()


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

    elif turnType == "buy arrow":
         BuyArrow()


    IO.drawFrame()
    turnNum += 1



class NewTrivia:
    UsedTrivia = []

    def __init__(self):
        self.newGame()
    

    def TriviaText():

        IO.displayText = "dfdskalfjdsklajfkldsa"
        IO.drawFrame()

    def newGame(self):
        # call at some point during the process of a game starting? might not be necessary
        # eventually UsedTrivia should be stored in a file when the game is closed (if there's a run in progress), and there should be a Trivia.loadGame() function that reads that file
        self.UsedTrivia = []
        knownSecrets = open("TriviaFiles/KnownSecrets.txt", "w")
        knownSecrets.write("")
        knownSecrets.close()

    def challenge(self, needCorrect, maxAttempts, player):
        # call when player action prompts a trivia battle (buying a secret, fighting the wumpus, buying arrows, etc.)
        # needCorrect and maxAttempts can be int or str
        # player is the object
        # returns True on success, False on failure (and 1 on death by bankruptcy?) (maybe change to 1, 0, 2?)
        IO.displayText = ("the player has " + str(maxAttempts) + " tries to get " + str(needCorrect) + " questions right")
        IO.drawFrame()

        correct = 0
        attempts = 0
        for i in range(int(maxAttempts)):
            if player.coins > 0:
                player.coins -= 1
            else:
                IO.displayText = ("no coins, can't answer trivia")
                IO.drawFrame()
                return False
            if (self.askQuestion()):
                correct += 1
            attempts += 1
            if (correct >= int(needCorrect)):
                return True
        return False

    def askQuestion(self):
        # used only by Trivia Object
        # right returns True, wrong returns False

        allTriviaFile = open("TriviaFiles/TriviaQA.txt", "r")
        allTrivia = allTriviaFile.readlines()
        allTriviaFile.close()

        questionNum = 0
        numUnusedTrivia = 0

        # count how many used and unused questions are in the QA file
        for line in allTrivia:
            if (line[0] != 'q'):
                continue
            if (self.UsedTrivia.count(questionNum) == 0):
                numUnusedTrivia += 1
            questionNum += 1
        
        if numUnusedTrivia == 0:
            IO.displayText = ("all trivia questions have been used")
            IO.drawFrame()

        # choose a random unused trivia question
        chosenQNum = random.randrange(0, numUnusedTrivia)
        
        list.sort(self.UsedTrivia)
        for usedQNum in self.UsedTrivia:
            if (usedQNum <= chosenQNum):
                chosenQNum += 1
        
        self.UsedTrivia.append(chosenQNum)
        question = allTrivia[chosenQNum * 2]
        questionText = question[2:] # what the player will be asked
        isWritten = (question[1] == 'w')
        answerLine = allTrivia[chosenQNum * 2 + 1][:-1] # line holding answers (includes all choices), does not include line break
        correctAnswers = []
        # written answer question
        if isWritten:
            correctAnswers = answerLine.split("|")
        # multiple choice question
        else:
            # make a list of the available choices, with the leading c or w
            choices = answerLine.split("|")
            random.shuffle(choices)
            questionText += "Choices:\n"
            for choice in choices:
                questionText += '\t' + choice[1:] + '\n'
                if choice[0] == 'c':
                    correctAnswers.append(choice[1:])
            choices = [choice[1:] for choice in choices] # remove leading c/w
        while True:
            playerAnswer = IO.getInput(questionText)
            if isWritten or playerAnswer in choices:
                break
            IO.displayText = (playerAnswer + " is invalid. Type one of the given choices.")
            IO.drawFrame()

        if str(playerAnswer).lower() in correctAnswers:
            IO.displayText = ("Correct!")
            IO.drawFrame()

            return True
        else:
            #print("Sorry! The correct answer was " + allTrivia[chosenQNum * 2 + 1][:-1] + ".")
            if len(correctAnswers) == 1:
                IO.displayText = ("Sorry! The correct answer was: " + correctAnswers[0])
                IO.drawFrame()
            else:
                message = "Sorry! The acceptible answers were: "
                for answer in correctAnswers:
                    message += "\n\t" + answer
                IO.displayText = (message)
                IO.drawFrame()

            return False
    
    # generate a message to send based on distance from player to a hazard/wumpus
    def getDistSecret(self, cave, locations, playerRoom, wumpRoom, type):
        if type == "wumpus":
            distance = cave.getDist(playerRoom, wumpRoom)
            return "The wumpus is " + str(distance) + " caverns away from you."
        elif type == "bat":
            allRooms = locations.getHazards()
            # get a list of two room numbers, which are the two that have a bat
            batRooms = [index for index in range(len(allRooms)) if allRooms[index] == "BAT"]
            # find which bat is closer to the player
            firstDistance = cave.getDist(playerRoom, batRooms[0])
            secondDistance = cave.getDist(playerRoom, batRooms[1])
            distance = min(firstDistance, secondDistance)
            return "The nearest super bat is " + str(distance) + " caverns away from you."
        elif type == "pit":
            allRooms = locations.getHazards()
            # get a list of two room numbers, which are the two that have a pit
            pitRooms = [index for index in range(len(allRooms)) if allRooms[index] == "PIT"]
            # find which pit is closer to the player
            firstDistance = cave.getDist(playerRoom, pitRooms[0])
            secondDistance = cave.getDist(playerRoom, pitRooms[1])
            distance = min(firstDistance, secondDistance)
            return "The nearest bottomless pit is " + str(distance) + " caverns away from you."

    def getSecret(self, locations, cave, playerRoom, wumpRoom):
        # call when player successfully buys a secret
        # pass gameLocations as argument
        # i think i'll need the cave to be passed so i can find how far away something is (in terms of how many turns it would take to get there) (this could be the same function as what's used for checking for warnings)
        # chooses a random secret from a file of secrets or from trivia answers
        # returns the secret as a string
        # adds the secret to a file of known secrets
        # secrets can be (1=common, 5=rare):
        #   (1) information about the location of a hazard or wumpus (how close it is to you, what the nearest wumpus/hazard is)
        #   (2) "lore" or information that will help solve trivia
        #   (3) a list of some trivia answers (without the question)
        #   (5) a partial map of the cave?
        # all of these next ones will be in terms of distance, not room number (they're arbitrary/incorrect room numbers now because it's easier, as a placeholder)
        if random.random() < 0.3:
            secret = self.getDistSecret(cave, locations, playerRoom, wumpRoom, "bat")
        elif random.random() < 0.5:
            secret = self.getDistSecret(cave, locations, playerRoom, wumpRoom, "pit")
        elif random.random() < 0.7:
            secret = self.getDistSecret(cave, locations, playerRoom, wumpRoom, "wumpus")
        else:
            secret = "The wumpus likes warm colors"
        knownSecrets = open("TriviaFiles/KnownSecrets.txt", "a")
        # next line should be modified so you don't have an extra \n at end of file, maybe
        knownSecrets.write(secret + "\n")
        knownSecrets.close()
        return secret
    
    def getKnownSecrets(self):
        # returns all known secrets from a file, as an array of strings
        # intention: player can look at a notebook to see all the secrets they've gleaned (maybe should include trivia they've been asked)
        knownSecrets = open("TriviaFiles/KnownSecrets.txt", "r")
        secrets = knownSecrets.read()
        knownSecrets.close()
        # remove the trailing \n
        secrets = secrets[:-1]
        return secrets
    
# temporary player object for testing (either the object or the class works)
#class Plr:
#    def __init__(self):
#        self.coins = 40
#PlayerObj = Plr()
#class PlayerObj:
#    coins = 12
#print(PlayerObj.coins)
#print(Trivia.challenge(2, 3, PlayerObj))
#print(PlayerObj.coins)

#Trv = Trivia()
#Trv.challenge(3, 5, PlayerObj)
#Trv.getSecret(0, 0)
#Trv.getKnownSecrets()