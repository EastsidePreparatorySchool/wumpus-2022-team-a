import random
from CaveObject import Cave

class LazyWumpus:
    wumpState = "ASLEEP"
    wumpPos = 0
    turnsSinceLastMove = 0
    # successive moves
    turnsMoved = 0
    turnsToMove = 0
    maximumRoomsMove = 1

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
        # return wumpState

    def changeToDead(self):
        self.wumpState = "DEAD"
        # return wumpState

    def changeToSleep(self):
        self.wumpState = "ASLEEP"
        # return wumpState

    def setTurnsToMove(self, num):
        self.turnsToMove = num

    def setMaximumRoomsMove(self, num):
        self.maximumRoomsMove = num

    def arrowMiss(self):
        return random.randint(1, 2)

    def trivia(self):
        return random.randint(1, 3)

    def moveWumpus(self, cave):
        # global wumpPos
        # global moveTurn

        # self.wumpState = "MOVING"
        # moveTurn = GameController2.getTurnNum()

        possiblePos = cave.getConnections(self.getWumpPos())
        self.wumpPos = possiblePos[random.randint(0, 5)]

        # return self.wumpPos

    def endTurnMove(self, cave, turnNum):
        global wumpPos
        global wumpState
        print("Wumpus is " + self.wumpState +
              " and in room " + str(self.wumpPos))
        if(self.wumpState == "AWAKE" and self.turnsMoved < self.turnsToMove):
            # move wumpus 1 room and update
            # choose random room to move to
            roomsToMove = random.randint(1, self.maximumRoomsMove)
            for i in range (0, roomsToMove): self.moveWumpus(cave)
            self.turnsMoved += 1
            # print("wumpus has moved to room " + str(connections[roomIndex]))
        elif(self.wumpState == "AWAKE" and self.turnsSinceLastMove < 2):
            self.turnsSinceLastMove += 1 
        else:
            # otherwise, wumpus is asleep and update variables
            self.wumpState = "ASLEEP"
            self.turnsSinceLastMove += 1
            self.turnsMoved = 0
                # print("wumpus is asleep and in room " + str(self.wumpPos))
            # IF WUMPUS IS DEFEATED IN TRIVIA, NEED TO CALL changeToAwake() from game control


    
