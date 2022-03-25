class Player:
    arrows = 0
    coins = 0
    pos = 0

    def __init__(self):
        self.arrows = 3
        self.coins = 0
        self.pos = 0
    
    def computeEndScore(self, wumpusState, turns):
        newScore = 100 - turns + Player.coins + 5 * Player.arrows + (50 if wumpusState == "DEAD" else 0)
        return newScore

    def useArrow(self):
        self.arrows -= 1