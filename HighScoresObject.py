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

    # no parameters
    # returns the top ten high scores as a list of strings
    # Scores are ordered by the list indexing - top score at 
    # index 0, bottom at index 9, etc.
    def getHighScores():
        with open("HighScores.txt", "r") as file1: 
            CurrentHighScoresList = file1.read().splitlines()
            return CurrentHighScoresList
    
    # Takes in a user name and the user's score, compares it to the current 
    # top ten scores, and adds it in the appropriate location in the list
    # if at all
    # No return
    # STILL NEED TO IMPLEMENT
    def addHighScore(UserName, UserScore): 
        pass 