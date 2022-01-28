from numpy import true_divide
import random

# from GameControl import GameControl
from cave import Cave
from Player import Player
from LazyWumpusObject import LazyWumpusObject


class GameLocations:
    cave = Cave()
    playerPos = 0
    wumpusPos = 0
    wumpusState = "ASLEEP"
    hazards = []

    def __init__(playerPos):
        self.playerPos = playerPos

        hazardPos = random.sample(range(1, 31), 4)
        hazards[hazardPos[0]] = "PIT"
        hazards[hazardPos[1]] = "PIT"
        hazards[hazardPos[2]] = "BAT"
        hazards[hazardPos[3]] = "BAT"
        
    
    def shootArrow(targetPos):
        if targetPos == wumpusPos:
            # GameControl.endGame()
            return True
        
        wumpusState = "AWAKE"
        for i in range(2):
            LazyWumpusObject.moveWumpus()
        return False

    def warnPlayer():
        possibleCaves = Cave.get_connected()
        possibleHazards = []

        for cave in possibleCaves:
            if cave in hazards.keys():
                possibleHazard.append(hazards.get(cave))

    def getSecret():
        pass