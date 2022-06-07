class Player:
    arrows = 0
    coinsNow = 0
    coinsAll = 0
    pos = 0

    def __init__(self):
        self.arrows = 3
        self.coinsNow = 3
        self.coinsAll = 3
        self.pos = 0
    
    def computeEndScore(self, wumpusState, turns):
        newScore = 100 - turns + Player.coinsNow + 5 * Player.arrows + (50 if wumpusState == "DEAD" else 0)
        return newScore

    def useArrow(self):
        self.arrows -= 1