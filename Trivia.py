import random

class Trivia:
    UsedTrivia = []

    def challenge(needCorrect, maxAttempts):
        # call when player action prompts a trivia battle (buying a secret, fighting the wumpus, buying arrows, etc.)
        # needCorrect and maxAttempts can be int or str
        # returns True on success, False on failure
        print("the player has " + str(maxAttempts) + " tries to get " + str(needCorrect) + " questions right")
        correct = 0
        attempts = 0
        for i in range(int(maxAttempts)):
            if (Trivia.askQuestion()):
                correct += 1
            attempts += 1
            if (correct >= int(needCorrect)):
                return True
        return False

    def askQuestion():
        # used only by Trivia Object
        # calls a Player function to decrement gold (still need to do)
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
    
    def getSecret():
        # call when player successfully buys a secret
        # chooses a random secret from a file of secrets or from trivia answers
        # returns the secret as a string
        # adds the secret to a file of known secrets
        pass
    
    def knownSecrets():
        # returns all known secrets from a file, as an array of strings
        pass

print(Trivia.challenge(2, 3))