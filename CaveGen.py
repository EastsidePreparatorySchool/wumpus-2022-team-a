import operator
import random

def makeAllAccessible(cave, hazards):
    current = 0
    fringe = []
    visited = []

    for c in cave.getAdjacent(current):
        if not isInAccessibilityFringe(c, current, fringe) and c not in visited:
            fringe.append((cave.getNumDualConnections(current, c), current, c))

    while fringe:
        # make fringe priority queue based on num of connections
        fringe = sorted(fringe, key=operator.itemgetter(0))

        # get new node
        newConnection = getRandomMinFromAccessibilityFringe(fringe)
        current = newConnection[1]
        other = newConnection[2]
        if current not in visited: visited.append(current)

        # if not too many connections
        if len(cave.getConnections(other)) < 3 and len(cave.getConnections(current)) < 3:
            # add connection
            cave.addConnection(other, current)
            updateAccessibilityFringe(cave, fringe)
            if other not in visited: visited.append(other)
        
        if areAllAccessible(cave)[0]:
            return

        # add neighbors to fringe
        for c in cave.getAdjacent(other):
            if not isInAccessibilityFringe(c, other, fringe) and c not in visited:
                fringe.append((cave.getNumDualConnections(other, c), other, c))

    # make connections to each of the hazards
    for h in hazards:
        other = random.choice(cave.getAdjacent(h))
        if len(cave.getConnections(h)) < 3 and len(cave.getConnections(other)) < 3:
            cave.addConnection(h, other)
            updateAccessibilityFringe(cave, fringe)

def isInAccessibilityFringe(c, other, fringe):
    for f in fringe:
        if f[1] == c or f[2] == c:
            if f[1] == other or f[2] == other:
                return True

    return False

def updateAccessibilityFringe(cave, fringe):
    for i in range(len(fringe)):
        fringe[i] = (cave.getNumDualConnections(fringe[i][1], fringe[i][2]), fringe[i][1], fringe[i][2])

    fringe = sorted(fringe, key=operator.itemgetter(0))

def getRandomMinFromAccessibilityFringe(fringe):
    fringe = sorted(fringe, key=operator.itemgetter(0))
    minVal = fringe[0][0]
    options = [f for f in fringe if f[0] == minVal]

    returnVal = random.choice(options)
    return fringe.pop(fringe.index(returnVal))

def areAllAccessible(cave):
    current = 0
    fringe = []
    fringe.extend(cave.getConnections(current))
    visited = []
    
    accessible = []

    while fringe:
        current = fringe.pop()
        visited.append(current)
        for c in cave.getConnections(current):
            if c not in visited and c not in accessible: fringe.append(c)

        accessible.append(current)

    accessible.sort()
    allAccessible = True
    for i in range(30):
        if i not in accessible:
            allAccessible = False
    
    return allAccessible, accessible
        
    
def makeMoreConnections(cave, iterations):
    for i in range(iterations):
        # make connections if possible
        current = cave.getRandomCavern()
        other = random.choice(cave.getAdjacent(current))

        if len(cave.getConnections(current)) < 3 and len(cave.getConnections(other)) < 3:
            cave.addConnection(current, other)