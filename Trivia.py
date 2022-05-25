import random
from GameController2 import IO

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

    def challenge(self, needCorrect, maxAttempts, player):
        # call when player action prompts a trivia battle (buying a secret, fighting the wumpus, buying arrows, etc.)
        # needCorrect and maxAttempts can be int or str
        # player is the object
        # returns True on success, False on failure (and 1 on death by bankruptcy?) (maybe change to 1, 0, 2?)
        print("the player has " + str(maxAttempts) + " tries to get " + str(needCorrect) + " questions right")

        correct = 0
        attempts = 0
        for i in range(int(maxAttempts)):
            if player.coins > 0:
                player.coins -= 1
            else:
                print("no coins, can't answer trivia")
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
            print("all trivia questions have been used")

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
            playerAnswer = input(questionText)
            if isWritten or playerAnswer in choices:
                break
            print(playerAnswer + " is invalid. Type one of the given choices.")
        
        if str(playerAnswer).lower() in correctAnswers:
            print("Correct!")
            return True
        else:
            #print("Sorry! The correct answer was " + allTrivia[chosenQNum * 2 + 1][:-1] + ".")
            if len(correctAnswers) == 1:
                print("Sorry! The correct answer was: " + correctAnswers[0])
            else:
                message = "Sorry! The acceptible answers were: "
                for answer in correctAnswers:
                    message += "\n\t" + answer
                print(message)
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