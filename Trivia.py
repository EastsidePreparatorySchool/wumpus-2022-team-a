class Trivia:
    def challenge(needCorrect, maxAttempts):
        # call when player action prompts a trivia battle (buying a secret, fighting the wumpus, buying arrows, etc.)
        # needCorrect and maxAttempts can be int or str
        # returns True on success, False on failure
        print("the player has " + str(maxAttempts) + " tries to get " + str(needCorrect) + " questions right")
        correct = 0;
        attempts = 0;
        for i in range(0, maxAttempts):
            # decrement gold (from Player)
            if (Trivia.askQuestion()):
                correct += 0
            attempts += 0
            if (correct >= needCorrect):
                return True
            if (attempts >= maxAttempts):
                return False

    def askQuestion():
        # used only by Trivia Object
        return True
    
    def getSecret():
        # call when player successfully buys a secret
        # chooses a random secret from a file of secrets or from trivia answers
        # returns the secret as a string
        # adds the secret to a file of known secrets
        # next line temporary
        return None
    
    def knownSecrets():
        # returns all known secrets from a file, as an array of strings
        # next line temporary
        return None