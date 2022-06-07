class HighScores: 

    scoresDict = {}
    # called once when object is first made to fill dictionary with current scores from file
    def __init__(self): 
        with open("HighScores.txt", "r") as file1:
            for currentLine in file1: 
                splitStringList = currentLine.split(' - ')
                # insert into list with key as name and value as score
                self.scoresDict[splitStringList[0]] = int(splitStringList[1])
            file1.close()

    # pass in player name as a string and get their specific high score, or -1 if it doesn't exist
    def getPlayerScore(self, playerName):
        return self.scoresDict.get(playerName, -1)

    # return all the high scores as a list of strings
    # each string is one high score (name, score)
    def getHighScores(self): 
        # print(self.scoresDict)
        # print("Current top scores: ")
        highScoresList = []
        count = 1
        for x in sorted(self.scoresDict, key=self.scoresDict.get, reverse=True): 
            if count < 11:
                # print(str(count) + ". ", x, " -- ", self.scoresDict[x])
                highScoresList[count - 1] = str(count) + ". ", x, " -- ", self.scoresDict[x]
                count += 1
                #print(x, " -- ", self.scoresDict[x])
            # get rid of any names and values that weren't in the top 10 scores
            else: 
                self.scoresDict.pop(x)
            count += 1
        return highScoresList
    
    # add a high score to the dictionary
    def addHighScore(self, userName, userScore): 
        self.scoresDict[userName] = userScore

    # this should be called once before the game exits so that the new high scores from this run can be saved
    # the idea is that if the player wants to play multiple times before exiting (and save the scores), the scores
    # only have to be written to the file once to be saved
    def writeHighScores(self): 
        with open("HighScores.txt", "w") as file1: 
            for name, score in self.scoresDict.items(): 
                print(name + " - " + str(score), file=file1)
        file1.close()