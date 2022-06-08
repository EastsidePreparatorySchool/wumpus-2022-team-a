import random
import math
import IO
import MainObjects

class Trivia:
    UsedTrivia = []

    def __init__(self):
        self.newGame()
    
    def newGame(self):
        # call at some point during the process of a game starting? might not be necessary
        # eventually UsedTrivia should be stored in a file when the game is closed (if there's a run in progress), and there should be a Trivia.loadGame() function that reads that file
        self.UsedTrivia = []
        knownSecrets = open("TriviaFiles/KnownSecrets.txt", "w")
        knownSecrets.write("")
        knownSecrets.close()

    def challenge(self, needCorrect, maxAttempts):
        # call when player action prompts a trivia battle (buying a secret, fighting the wumpus, buying arrows, etc.)
        # needCorrect and maxAttempts can be int or str
        # player is the object
        # returns True on success, False on failure (and 1 on death by bankruptcy?) (maybe change to 1, 0, 2?)
        
        player = MainObjects.player

        # wait for player to press enter
        IO.getInput()
        IO.write("You have " + str(maxAttempts) + " tries to get " + str(needCorrect) + " questions right")

        correct = 0
        attempts = 0
        for i in range(int(maxAttempts)):
            if (self.askQuestion()):
                correct += 1
            if player.coinsNow > 0:
                player.coinsNow -= 1
            else:
                IO.write("You have no coins to pay for trivia.")
                IO.getInput()
                return False
            attempts += 1
            if (correct >= int(needCorrect)):
                IO.getInput()
                return True
        IO.getInput()
        return False

    def askQuestion(self):
        # used only by Trivia Object
        # right returns True, wrong returns False

        fileData = self.getTriviaFileData()
        allTrivia = fileData[0]
        # don't need fileData[1] which is number of questions
        numUnusedTrivia = fileData[2]
        
        if numUnusedTrivia == 0:
            print("oh no! all trivia questions have been used")

        # choose a random unused trivia question
        chosenQNum = random.randrange(0, numUnusedTrivia)
        
        list.sort(self.UsedTrivia)
        for usedQNum in self.UsedTrivia:
            if (usedQNum <= chosenQNum):
                chosenQNum += 1
        
        self.UsedTrivia.append(chosenQNum)
        question = allTrivia[chosenQNum * 2]
        questionText = self.removeTrailingLineBreak(question[2:]) # what the player will be asked
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
            questionText += " Choices:   "
            for choice in choices:
                #questionText += '\t' + choice[1:] + '\n'  escape characters dont work in pygame output
                questionText += choice[1:] + "   "
                if choice[0] == 'c':
                    correctAnswers.append(choice[1:])
            choices = [choice[1:] for choice in choices] # remove leading c/w
        while True:
            playerAnswer = IO.getInput(questionText)
            if isWritten or playerAnswer in choices:
                break
            IO.write(playerAnswer + " is invalid. Type one of the given choices.")
        
        if str(playerAnswer).lower() in correctAnswers:
            IO.write("Correct!")
            return True
        else:
            IO.write("Sorry! An acceptable answer was: " + correctAnswers[0])
            # note: in the case of multiple correct answers, this previously outputted all
            # acceptable answers. but that can take too much space so only output 1st in file
            return False
    
    # returns tuple about file. format: (list of lines, num of questions, num unused)
    def getTriviaFileData(self):
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
        
        return (allTrivia, questionNum, numUnusedTrivia)

    
    # generate a message to send based on distance from player to a hazard/wumpus
    def getDistSecret(self, type):
        player = MainObjects.player
        cave = MainObjects.cave
        wumpus = MainObjects.wumpus
        locations = MainObjects.location

        playerRoom = player.pos
        if type == "wumpus":
            wumpRoom = wumpus.wumpPos
            distance = cave.getDist(playerRoom, wumpRoom)
            return "The wumpus is " + str(distance) + " caverns away from you."
        elif type == "bat":
            allRooms = locations.getHazards()
            # get a list of two room numbers, which are the two that have a bat
            batRooms = [index for index in range(len(allRooms)) if allRooms[index] == "BAT"]
            print(batRooms[0])
            print(batRooms[1])
            # find which bat is closer to the player
            firstDistance = cave.getDist(playerRoom, batRooms[0])
            secondDistance = cave.getDist(playerRoom, batRooms[1])
            # idk why one of first and second distance would be null, but that's happening so
            # this is to sort of fix it
            if firstDistance is None:
                distance = secondDistance
            elif secondDistance is None:
                distance = firstDistance
            else:
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

    # returns a secret that says whether the wumpus is nearby
    def getWumpCloseSecret(self):
        player = MainObjects.player
        cave = MainObjects.cave
        wumpus = MainObjects.wumpus
        if cave.getDist(player.pos, wumpus.getWumpPos()) < 3:
            return "The wumpus is within 2 caverns of you."
        else:
            return "The wumpus is farther than 2 caverns away from you."
    
    # returns a secret that's an item's room number. type is bat, pit, player, or wumpus
    def getPosSecret(self, type):
        locations = MainObjects.location
        secret = "There is a " + type + " in room "
        allRooms = locations.getHazards()
        # find pos of a bat or a pit
        if type == "bat" or type == "pit":
            # find a random room with this type of item in it
            thisTypeRooms = [index for index in range(len(allRooms)) if allRooms[index] == type.upper()]
            secret += str(thisTypeRooms[random.randrange(2)])
        # find pos of player or wump (neither are in hazards)
        if type == "player":
            secret += str(MainObjects.player.pos)
        if type == "wumpus":
            secret += str(MainObjects.wumpus.wumpPos)
        
        secret += "."
        return secret

    # low-context, obfuscated answer to a trivia question
    def getTriviaSecret(self):
        secret = "#-3&"
        triviaFileData = self.getTriviaFileData()
        allTrivia = triviaFileData[0]
        numOfQuestions = triviaFileData[1]
        # find a random answer line
        questionLineNum = random.randrange(numOfQuestions) * 2
        answerLineNum = questionLineNum + 1
        questionLine = allTrivia[questionLineNum]
        answerLine = allTrivia[answerLineNum]
        # look for a correct answer
        isWritten = (questionLine[1] == 'w')
        answers = answerLine.split("|") # either corrects (for written), or choices
        # find correct answers and choose one of them at random
        if not isWritten:
            # refine answers to only the correct ones
            answers = [choice[1:] for choice in answers if choice[0] == 'c']
        chosenAnswer = answers[random.randrange(len(answers))]
        secret += self.removeTrailingLineBreak(chosenAnswer)
        secret += "%@M-$?"
        return secret

    def getSecret(self):
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
        choice = random.randrange(4, 10) # temporarily removing 0,1,2,3 bc getdist isn't working
        if choice == 0:
            secret = self.getDistSecret("bat")
        elif choice == 1:
            secret = self.getDistSecret("pit")
        elif choice == 2:
            secret = self.getDistSecret("wumpus")
        elif choice == 3:
            secret = self.getWumpCloseSecret()
        elif choice == 4:
            secret = self.getPosSecret("bat")
        elif choice == 5:
            secret = self.getPosSecret("pit")
        elif choice == 6:
            secret = self.getPosSecret("wumpus")
        elif choice == 7:
            secret = self.getPosSecret("player")
        elif choice == 8:
            secret = self.getTriviaSecret()
        else:
            # these cases should each be fairly improbable. several of them are hints to trivia
            # but generally these are not useful.
            secondChoice = random.randrange(6)
            if secondChoice == 0:
                secret = "The wumpus likes warm colors."
            elif secondChoice == 1:
                secret = "Two bats live in this cave."
            elif secondChoice == 2:
                secret = "Many languages are spoken in NYC."
            elif secondChoice == 3:
                secret = "The original Hunt the Wumpus was created in 1973."
            elif secondChoice == 4:
                secret = "The walls of this cave drown out all exterior sounds, even the roar of a sperm whale."
            elif secondChoice == 5:
                secret = "This game is coded in Python."
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
    
    # remove \n at end of line
    def removeTrailingLineBreak(self, string):
        if string[-1] == '\n':
            string = string[:-1]
        return string