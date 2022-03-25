import random

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
            if (self.askQuestion()):
                correct += 1
            if player.coins > 0: # this if/else should maybe be before asking the question
                player.coins -= 1
            else:
                # will need to tell Control about loss by returning a different value
                print("lose game due to trying to pay coins when broke")
                return "Bankrupt"
            attempts += 1
            if (correct >= int(needCorrect)):
                return "W"
        return "L"

    def askQuestion(self):
        # used only by Trivia Object
        # right returns True, wrong returns False

        allTriviaFile = open("TriviaFiles/TriviaQA.txt", "r")
        allTrivia = allTriviaFile.readlines()
        allTriviaFile.close()

        questionNum = 0
        numUnusedTrivia = 0

        # count how many questions are in the QA file
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
        answer = input(allTrivia[chosenQNum * 2][1:])
        # ignoring the last character of each line of the file, which is \n
        if (str(answer).lower() == allTrivia[chosenQNum * 2 + 1][:-1]):
            print("Correct!")
            return True
        else:
            print("Sorry! The correct answer was " + allTrivia[chosenQNum * 2 + 1][:-1] + ".")
            return False
    
    def getSecret(self, locations, cave):
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
        if random.random() < 0.2:
            #secret = "A bottemless pit is in room " + str(locations.pit1)
            secret = "A bottemless pit is in room 4"
        elif random.random() < 0.2:
            secret = "A bottomless pit is in room 4"
        elif random.random() < 0.2:
            secret = "A super bat is in room 4"
        elif random.random() < 0.2:
            secret = "A super bat is in room 4"
        elif random.random() < 0.3:
            secret = "The wumpus is in room 4"
        else:
            secret = "The wumpus likes warm colors"
        print(secret)
        knownSecrets = open("TriviaFiles/KnownSecrets.txt", "a")
        # next line should be modified so you don't have an extra \n at end of file, maybe
        knownSecrets.write(secret + "\n")
        knownSecrets.close()
        return secret
    
    def getKnownSecrets(self):
        # returns all known secrets from a file, as an array of strings
        # intention: player can look at a notebook to see all the secrets they've gleaned (maybe should include trivia they've been asked)
        knownSecrets = open("TriviaFiles/KnownSecrets.txt", "r")
        secretsList = knownSecrets.read()
        knownSecrets.close()
        print(secretsList)
        return secretsList
    
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