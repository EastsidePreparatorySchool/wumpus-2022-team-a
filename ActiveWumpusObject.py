import random
from CaveObject import Cave


class ActiveWumpus:
    wumpState = "ASLEEP"
    wumpPos = 1
    localTurnNum = 0
    turnsSinceLastMove = 0
    # successive moves
    turnsMoved = 0
    turnsToMove = 0
    maximumRoomsMove = 1

    def init(self):
        self.wumpState = "ASLEEP"
        self.wumpPos = 1
        self.localTurnNum = 0
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

        # SHOULDNT THIS BE GET CONNECTIONS?
        possiblePos = cave.getConnections(self.getWumpPos())
        self.wumpPos = possiblePos[random.randint(0, 5)]

        # return self.wumpPos

    def possibleTeleport(self):
        if (random.randint(1, 20) == 1):
            self.wumpPos = random.randint(2, 30)

    def endTurnMove(self, cave, turnNum):
        global wumpPos
        global wumpState
        print("Wumpus is " + self.wumpState +
              " and in room " + str(self.wumpPos))
        # 5% change the wumpus teleports to a new location
        if self.wumpState == "ASLEEP" and self.turnsSinceLastMove >= 5:
            # if asleep for 5 or more turns, there is a 20 + 10% for every turn greater
            # than five that we have not moved chance that the wumpus wakes up
            if(random.randint(1, 100) <= 50 + (10 * (self.turnsSinceLastMove - 5))):
                self.wumpState = "AWAKE"
                self.turnsToMove = random.randint(1, 3)
                # print("wumpus is " + self.wumpState + str(self.wumpPos))
            # if awake and hasn't moved for more than 3 turns in a row, keeps moving:
        if(self.wumpState == "AWAKE" and self.turnsMoved < self.turnsToMove):
            # move wumpus 1 room and update
            # choose random room to move to
            roomsToMove = random.randint(1, self.maximumRoomsMove)
            for i in range (0, roomsToMove): self.moveWumpus(cave)
            self.turnsMoved += 1
            # print("wumpus has moved to room " + str(connections[roomIndex]))
        else:
            # otherwise, wumpus is asleep and update variables
            self.wumpState = "ASLEEP"
            self.turnsSinceLastMove += 1
            self.turnsMoved = 0
                # print("wumpus is asleep and in room " + str(self.wumpPos))
            # IF WUMPUS IS DEFEATED IN TRIVIA, NEED TO CALL changeToAwake() from game control

    # curTurn = GameControl.getTurnNum()
    # if wumpState == "MOVING":
    #     if curTurn - moveTurn >= 2:
    #         wumpState = "ASLEEP"
