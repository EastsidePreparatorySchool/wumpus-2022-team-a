import random

class LazyWumpus:
    wumpState = "ASLEEP"
    wumpPos = 0
    localTurnNum = 0

    def __init__(self): 
        self.wumpState = "ASLEEP"
        self.wumpPos = 0
        self.localTurnNum = 0

    # accessor method for wumpPos for other objects
    def getWumpPos(self):
        return self.wumpPos
    
    # accessor method for wumpState for other objects
    def getWumpState(self):
        return self.wumpState

    def changeToAwake(self):
        global wumpState 
        wumpState = "AWAKE"
        return wumpState

    def changeToSleep(self):
        global wumpState
        wumpState = "ASLEEP"
        return wumpState

    def arrowMiss(self):
        return random.randint(1, 2)

    def trivia(self):
        return random.randint(1, 3)

    def moveWumpus(self):
        global wumpState
        global wumpPos
        global moveTurn

        wumpState = "MOVING"
        #moveTurn = GameController2.getTurnNum()

        possiblePos = cave.getAdjacent(wumpPos)
        wumpPos = possiblePos[random.randint(0, 5)]
        
        return wumpPos    

    # curTurn = GameControl.getTurnNum()
    # if wumpState == "MOVING":
    #     if curTurn - moveTurn >= 2:
    #         wumpState = "ASLEEP"

    
