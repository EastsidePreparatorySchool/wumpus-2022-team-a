class Player:
    arrows = 0
    coins = 0
    turns = 0

    def __init__():
        self.arrows = 3
        self.coins = 0
        self.turns = 0
    
    def computeEndScore():
        newScore = 100 - turns + coins + 5 * arrows + (50 if LazyWumpusObject.getWumpState() == "DEAD" else 0)
        HighSchoresObject.addHighScore(newScore)