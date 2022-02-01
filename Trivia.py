import random

class Trivia:
    UsedTrivia = []
    def newGame():
        # call at some point during the process of a game starting? might not be necessary
        # eventually UsedTrivia should be stored in a file when the game is closed (if there's a run in progress), and there should be a Trivia.loadGame() function that reads that file
        Trivia.UsedTrivia = []

    def challenge(needCorrect, maxAttempts, player):
        # call when player action prompts a trivia battle (buying a secret, fighting the wumpus, buying arrows, etc.)
        # needCorrect and maxAttempts can be int or str
        # player is the object
        # returns True on success, False on failure (and 1 on death by bankruptcy?) (maybe change to 1, 0, 2?)
        print("the player has " + str(maxAttempts) + " tries to get " + str(needCorrect) + " questions right")

        correct = 0
        attempts = 0
        for i in range(int(maxAttempts)):
            if (Trivia.askQuestion()):
                correct += 1
            if player.coins > 0: # this if/else should maybe be before asking the question
                player.coins -= 1
            else:
                # will need to tell Control about loss by returning a different value
                print("lose game due to trying to pay coins when broke")
            attempts += 1
            if (correct >= int(needCorrect)):
                return True
        return False

    def askQuestion():
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
            if (Trivia.UsedTrivia.count(questionNum) == 0):
                numUnusedTrivia += 1
            questionNum += 1
        
        # choose a random unused trivia question
        chosenQNum = random.randrange(0, numUnusedTrivia)
        list.sort(Trivia.UsedTrivia)
        for usedQNum in Trivia.UsedTrivia:
            if (usedQNum <= chosenQNum):
                chosenQNum += 1
        
        Trivia.UsedTrivia.append(chosenQNum)
        answer = input(allTrivia[chosenQNum * 2][1:])
        # ignoring the last character of each line of the file, which is \n
        if (str(answer).lower() == allTrivia[chosenQNum * 2 + 1][:-1]):
            print("Correct!")
            return True
        else:
            print("Sorry! The correct answer was " + allTrivia[chosenQNum * 2 + 1][:-1] + ".")
            return False
    
    def getSecret(locations):
        # call when player successfully buys a secret
        # pass gameLocations as argument
        # chooses a random secret from a file of secrets or from trivia answers
        # returns the secret as a string
        # adds the secret to a file of known secrets
        pass
    
    def knownSecrets():
        # returns all known secrets from a file, as an array of strings
        # intention: player can look at a notebook to see all the secrets they've gleaned (maybe should include trivia they've been asked)
        pass
    
# temporary player object for testing (either the object or the class works)
#class Plr:
#    def __init__(self):
#        self.coins = 5
#PlayerObj = Plr()
#class PlayerObj:
#    coins = 12
#print(PlayerObj.coins)
#print(Trivia.challenge(2, 3, PlayerObj))
#print(PlayerObj.coins)