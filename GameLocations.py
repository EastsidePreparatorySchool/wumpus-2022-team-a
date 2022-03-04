import random

# from GameController2 import GameController2
# from cave import Cave
# from Player import Player
# from LazyWumpusObject import LazyWumpus

class GameLocations:
    hazards = {}

    def __init__(self):
        self.hazards = {}

    # Called by GameControl
    def getHazards():
        return GameLocations.hazards

    def spawnItems(self, wumpus, cave, player):
        hazards = GameLocations.getHazards()

        hazardPos = random.sample(range(1, 31), 4)
        hazards.get(hazardPos[0], "PIT")
        hazards.get(hazardPos[1], "PIT")
        hazards.get(hazardPos[2], "BAT")
        hazards.get(hazardPos[3], "BAT")

    # Called by GameControl
    def movePlayer(self, targetPos, wumpus, cave, player):
        BAT = "B"
        PIT = "P"
        WUMPUS = "W"
        WUMPUS_AND_BAT = "WB"
        WUMPUS_AND_PIT = "WP"

        wumpusPos = wumpus.getWumpPos()
        hazards = GameLocations.getHazards()

        for pos in GameLocations.hazards.keys():
            if pos == targetPos:
                if GameLocations.hazards[pos] == "PIT":
                    # Reset position to initial starting point (currently always 0)
                    playerPos = 0

                    if targetPos == wumpusPos:
                        return WUMPUS_AND_PIT
                        # "You encountered the Wumpus, but fell into a pit."
                    return PIT
                    # "You fell into a pit."
                
                elif hazards[pos] == "BAT":
                    playerPos == random.randint(1, 30)

                    b1 = 0
                    b2 = 0
                    bFound = False
                    p1 = 0
                    p2 = 0
                    pFound = False

                    for i in range(1, 31):
                        if hazards[i] == "BAT" and not bFound:
                            b1 = i
                            bFound = True
                        elif hazards[i] == "BAT":
                            b2 = i
                        elif hazards[i] == "PIT" and not pFound:
                            p1 = i
                            pFound = True
                        elif hazards[i] == "PIT":
                            p2 = i
                    
                    possiblePos = range(1, 31)
                    possiblePos.remove(b2, p1, p2)
                    newPos = random.sample(possiblePos, 1)
                    hazards.pop(b1)
                    hazards.add(newPos, "BAT")

                    if targetPos == wumpusPos:
                        return WUMPUS_AND_BAT
                        # "You encountered the Wumpus, but were saved by bats."
                    return BAT
                    # "You were moved by a bat."
        
        if targetPos == wumpusPos:
            return WUMPUS
            # "You encountered the Wumpus. Fight for your life."

    # Called by GameControl
    def shootArrow(self, targetPos, wumpus, cave, player):
        wumpusPos = wumpus.getWumpPos()

        if targetPos == wumpusPos:
            # End game in this case
            return True
        
        wumpus.arrowMiss()
        wumpus.changeToAwake()
        wumpus.moveWumpus()
        return False

    # Called by GameControl
    def getWarnings(self, wumpus, cave, player):
        hazards = GameLocations.getHazards()

        possibleCaves = cave.get_connected()
        possibleHazards = []

        for cave in possibleCaves:
            if cave in hazards.keys():
                possibleHazards.append(hazards.get(cave))
        
        if len(possibleHazards) > 0:
            return possibleHazards
        return None