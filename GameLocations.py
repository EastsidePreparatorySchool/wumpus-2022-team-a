import random
import MainObjects

# from GameController2 import GameController2
# from Cave import Cave
# from Player import Player
# from LazyWumpusObject import LazyWumpus

class GameLocations:
    hazards = {}

    def __init__(self):
        self.hazards = {}

    # Called by GameControl
    def getHazards(self):
        return self.hazards

    def spawnItemsRandom(self):
        hazards = self.getHazards()
        for i in range(30):
            hazards[i] = ""

        hazardPos = random.sample(range(1, 30), 4)
        hazards[hazardPos[0]] = "PIT"
        hazards[hazardPos[1]] = "PIT"
        hazards[hazardPos[2]] = "BAT"
        hazards[hazardPos[3]] = "BAT"
    
    def spawnItemsCustom(self, wumpus, spawnWumpPos):
        hazards = self.getHazards()
        for i in range(30):
            hazards[i] = ""

        p1 = 25
        p2 = 13
        b1 = 30
        b2 = 3

        hazards[p1] = "PIT"
        hazards[p2] = "PIT"
        hazards[b1] = "BAT"
        hazards[b2] = "BAT"
        wumpus.wumpPos = spawnWumpPos

    # Called by GameControl
    def checkHazards(self, currentPos, wumpus, cave, player):
        BAT = "B"
        PIT = "P"
        WUMPUS = "W"
        WUMPUS_AND_BAT = "WB"
        WUMPUS_AND_PIT = "WP"

        wumpusPos = wumpus.getWumpPos()
        hazards = self.getHazards()

        for pos in self.hazards.keys():
            if pos == currentPos:
                if self.hazards[pos] == "PIT":
                    # Reset position to initial starting point (currently always 0)
                    player.pos = 0

                    if currentPos == wumpusPos:
                        return WUMPUS_AND_PIT
                        # "You encountered the Wumpus, but fell into a pit."
                    return PIT
                    # "You fell into a pit."
                
                elif hazards[pos] == "BAT": 
                    #player.pos = random.randint(1, 30)  moving this line to control

                    #b1 = 0
                    b2 = 0
                    #bFound = False
                    p1 = 0
                    p2 = 0
                    pFound = False

                    for i in range(1, 30):
                        #if hazards[i] == "BAT" and not bFound:
                        #    b1 = i
                        #    bFound = True
                        if hazards[i] == "BAT":
                            b2 = i
                        elif hazards[i] == "PIT" and not pFound:
                            p1 = i
                            pFound = True
                        elif hazards[i] == "PIT":
                            p2 = i
                    
                    possiblePos = list(range(30))
                    possiblePos.remove(b2)
                    possiblePos.remove(p1)
                    possiblePos.remove(p2)
                    newPos = random.sample(possiblePos, 1)[0]
                    #hazards.pop(b1)
                    #hazards.pop(currentPos)  this causes an error in line 67 because it makes
                    #                         hazards[i] stop existing for one value
                    hazards[currentPos] = ""
                    hazards[newPos] = "BAT"

                    # print(self.getHazards())

                    if currentPos == wumpusPos:
                        return WUMPUS_AND_BAT
                        # "You encountered the Wumpus, but were saved by bats."
                    return BAT
                    # "You were moved by a bat."
        
        if currentPos == wumpusPos:
            return WUMPUS
            # "You encountered the Wumpus. Fight for your life."

    # Called by GameControl
    def shootArrow(self, targetPos, wumpus, cave, player):
        wumpusPos = wumpus.getWumpPos()

        if targetPos == wumpusPos:
            # End game in this case
            return True
        
        player.useArrow()

        wumpus.setTurnsToMove(wumpus.arrowMiss())
        wumpus.changeToAwake()
        return False

    # Called by GameControl
    def getWarnings(self):
        hazards = self.getHazards()
        wumpus = MainObjects.wumpus
        cave = MainObjects.cave
        player = MainObjects.player

        possibleCaves = cave.getConnections(player.pos)
        # possibleCaves = []
        # for currCave in range(30):
        #     if 0 < cave.getDist(currCave, player.pos) <= 2:
        #         possibleCaves.append(currCave)

        possibleHazards = []
        for currCave in possibleCaves:
            #if cave in hazards.keys():
                #possibleHazards.append(hazards.get(cave))
            possibleHazards.append(hazards.get(currCave))

        if wumpus.getWumpPos() in possibleCaves:
            possibleHazards.append("WUMPUS")
        
        return possibleHazards