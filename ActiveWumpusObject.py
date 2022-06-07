import random
from CaveObject import Cave

class ActiveWumpus:
    wumpState = "ASLEEP"
    # wumpus position
    wumpPos = 1
    # successive moves
    turnsMoved = 0
    turnsToMove = 0
    turnsSinceLastMove = 0
    # maximum number of rooms able to move to in a turn
    maximumRoomsMove = 1

    def init(self):
        self.wumpState = "ASLEEP"
        self.wumpPos = 1
        self.turnsSinceLastMove = 0
        self.turnsMoved = 0
        self.turnsToMove = 0
        self.maximumRoomsMove = 1

    # accessor method for wumpPos for other objects
    def getWumpPos(self):
        return self.wumpPos

    # accessor method for wumpState for other objects
    def getWumpState(self):
        return self.wumpState

    def changeToAwake(self):
        self.wumpState = "AWAKE"

    def changeToDead(self):
        self.wumpState = "DEAD"

    def changeToSleep(self):
        self.wumpState = "ASLEEP"

    # accessor method for setting the specific number of turns
    # wumpus should be moving depending on the context
    def setTurnsToMove(self, num):
        self.turnsToMove = num

    # accessor method for setting the specific number of turns
    # wumpus should be moving depending on the context
    def setMaximumRoomsMove(self, num):
        self.maximumRoomsMove = num

    # getter methods for random number of turns for wumpus to move
    def arrowMiss(self):
        return random.randint(1, 2)

    def trivia(self):
        return random.randint(1, 3)

    # method to move wumpus
    def moveWumpus(self, cave):
        possiblePos = cave.getConnections(self.getWumpPos())
        self.wumpPos = possiblePos[random.randint(0, 5)]

    # method to teleport the wumpus
    def possibleTeleport(self):
        if (random.randint(1, 20) == 1):
            self.wumpPos = random.randint(2, 30)

    def endTurnMove(self, cave, turnNum):
        global wumpPos
        global wumpState

        print("Wumpus is " + self.wumpState +
              " and in room " + str(self.wumpPos))
        
        if self.wumpState == "ASLEEP" and self.turnsSinceLastMove >= 5:
            # if asleep for 5 or more turns, there is a 20 + 10% extra chance  
            # every turn over five that the wumpus wakes up
            if(random.randint(1, 100) <= 50 + (10 * (self.turnsSinceLastMove - 5))):
                self.wumpState = "AWAKE"
                # choose random number of turns that wumpus will move in the 
                # next few turns 
                self.turnsToMove = random.randint(1, 3)

        # if awake and hasnt finished the number of turns supposed to move, keep moving:
        if(self.wumpState == "AWAKE" and self.turnsMoved < self.turnsToMove):
            # move wumpus 1 room and choose random room to move to
            roomsToMove = random.randint(1, self.maximumRoomsMove)
            for i in range (0, roomsToMove): self.moveWumpus(cave)
            self.turnsMoved += 1

        # wumpus should be asleep so update all variables  
        else: 
            self.wumpState = "ASLEEP"
            self.turnsSinceLastMove += 1
            self.turnsMoved = 0

