class HighScores: 
    
    # constructor
    # do I need any data fields? I can't think of any.
    # creates the file with each array element as a separate line
    def __init__(self): 
        defaultText = ["Sam - 0", "Keyan - 0", "Oliver - 0", "Sam - 0", "Andrei - 0", "Alan - 0", "Jonathan - 0"]
        with open("HighScores.txt", "w") as file1: 
            for x in range(len(defaultText)):
                # can either use this print or put new lines into the strings
                print(defaultText[x], file=file1)
            file1.close()

    # no parameters
    # returns the top ten high scores as a list of strings
    # Scores are ordered by the list indexing - top score at 
    # index 0, bottom at index 9, etc.
    def getHighScores(self):
        with open("HighScores.txt", "r") as file1: 
            CurrentHighScoresList = file1.read().splitlines()
            file1.close()
            return CurrentHighScoresList
    
    # Takes in a user name and the user's score, compares it to the current 
    # top ten scores, and adds it in the appropriate location in the list
    # if at all
    # No return
    def addHighScore(self, UserName, UserScore): 
        # newScore = GameControl.getHighScore()
        currentScoresArr = [] # currentScoresArr = {}
        with open("HighScores.txt", "r") as file1:
            currentLine = file1.readline()
            splitString = currentLine.split(' - ')
            print(splitString)
            for x in range(10):
                # currentScoresArr[splitString[0]] = splitString[1]
                currentScoresArr.append(splitString[2 * x]) 
                currentScoresArr.append(splitString[2 * x + 1])
                # print(splitString[0], splitString[1])
            print(currentScoresArr)
            file1.close()
        for x in range(len(currentScoresArr)//2): 
            if(UserScore < int(currentScoresArr[x * 2 + 1])): 
                currentScoresArr.insert(x, (UserName, UserScore))
        with open("HighScores.txt", "w") as file1: 
            if(len(currentScoresArr) >= 21): 
                for x in range(10):
                    print(currentScoresArr[2 * x] + " - " + currentScoresArr[2 * x + 1], file=file1)
            else: 
                for x in range(len(currentScoresArr) // 2): 
                    print(currentScoresArr[2 * x] + " - " + currentScoresArr[2 * x + 1], file=file1)
            file1.close()

# defaultText = ["Sam - 0", "Keyan - 0", "Oliver - 0", "Sam - 0", "Andrei - 0", "Alan - 0", "Jonathan - 0"]
# ["Sam", 0, "Keyan", 0, "Oliver", 0...]