from numpy import true_divide


class GameLocations:
    # cave = Cave()
    playerPos = 0
    wumpusPos = 0
    wumpusState = "ASLEEP"
    hazards = []

    def __init__(playerPos):
        self.playerPos = playerPos
    
    def shootArrow(targetPos):
        if targetPos == wumpusPos:
            # GameControl.endGame()
            return True
        
        wumpusState = "AWAKE"
        for i in range(2):
            LazyWumpusObject.moveWumpus()
        return False

    def warnPlayer():
        pass

    def getSecret():
        pass