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

    def moveWumpus():
        global wumpState
        global wumpPos

        wumpState = "MOVING"

        if wumpPos % 2 == 1:
            possiblePos = [
                (wumpPos + 6) % 30, 
                (wumpPos + 1),
                (wumpPos - 5) % 30,
                (wumpPos - 6) % 30,
                (wumpPos - 7) % 30,
                (wumpPos + 5) % 30
            ]
        else:
            possiblePos = [
                (wumpPos + 6) % 30, 
                (wumpPos + 1),
                (wumpPos - 5) % 30,
                (wumpPos - 6) % 30,
                (wumpPos - 7) % 30,
                (wumpPos + 5) % 30
            ]
        pass     