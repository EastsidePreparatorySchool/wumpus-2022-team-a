import random

class LazyWumpus:
    wumpState = "ASLEEP"
    wumpPos = 0
    localTurnNum = 0

    # accessor method for wumpPos for other objects
    def getWumpPos():
        return wumpPos
    
    # accessor method for wumpState for other objects
    def getWumpState():
        return wumpState

    def changeToAwake():
        global wumpState 
        wumpState = "AWAKE"
        return wumpState

    def changeToSleep():
        global wumpState
        wumpState = "ASLEEP"
        return wumpState

    def arrowMiss():
        return random.randint(1, 2)

    def trivia():
        return random.randint(1, 3)

    def moveWumpus():
        global wumpState
        global wumpPos
        global moveTurn

        wumpState = "MOVING"
        moveTurn = GameControl.getTurnNum()

        possiblePos = cave.getAdjacent(wumpPos)
        wumpPos = possiblePos[random.randint(0, 5)]
        
        return wumpPos    

    curTurn = GameControl.getTurnNum()
    if wumpState == "MOVING":
        if curTurn - moveTurn >= 2:
            wumpState = "ASLEEP"

    
