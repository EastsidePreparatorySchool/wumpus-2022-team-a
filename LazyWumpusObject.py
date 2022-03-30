import random
from cave import Cave

class LazyWumpus:
    wumpState = "ASLEEP"
    wumpPos = 0
    localTurnNum = 0

    def __init__(self): 
        self.wumpState = "ASLEEP"
        self.wumpPos = 1
        self.localTurnNum = 0

    # accessor method for wumpPos for other objects
    def getWumpPos(self):
        return self.wumpPos
    
    # accessor method for wumpState for other objects
    def getWumpState(self):
        return self.wumpState

    def changeToAwake(self):
        self.wumpState = "AWAKE"
        #return wumpState
    
    def changeToDead(self):
        self.wumpState = "DEAD"
        #return wumpState

    def changeToSleep(self):
        self.wumpState = "ASLEEP"
        #return wumpState

    def arrowMiss(self):
        return random.randint(1, 2)

    def trivia(self):
        return random.randint(1, 3)

    def moveWumpus(self, cave):
        #global wumpPos
        #global moveTurn

        self.wumpState = "MOVING"
        #moveTurn = GameController2.getTurnNum()

        possiblePos = cave.getAdjacent(self.getWumpPos())
        self.wumpPos = possiblePos[random.randint(0, 5)]
        
        #return self.wumpPos    

    # curTurn = GameControl.getTurnNum()
    # if wumpState == "MOVING":
    #     if curTurn - moveTurn >= 2:
    #         wumpState = "ASLEEP"

    
