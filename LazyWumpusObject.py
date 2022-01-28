class LazyWumpus:
    wumpState = "ASLEEP"
    wumpPos = 0

    # accessor method for wumpPos for other objects
    def getWumpPos():
        return wumpPos
    
    # accessor method for wumpState for other objects
    def getWumpState():
        return wumpState

    # call turn number from ?
    def changeState():
        global turnNum
        if turnNum >
        pass

    def moveWumpus():
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

    