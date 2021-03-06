import operator
import random

# collection of functions for generating the cave

def makeAllAccessible(cave, hazards):
    # main function, for generating a cave randomly
    # ensures that hazards are accounted for, and 
    # that every cavern is accessible

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
        if h != "":
            print(h)
            other = random.choice(cave.getAdjacent(h))
            if len(cave.getConnections(h)) < 3 and len(cave.getConnections(other)) < 3:
                cave.addConnection(h, other)
                updateAccessibilityFringe(cave, fringe)

def isInAccessibilityFringe(c, other, fringe):
    # checks to see if a connection is in the fringe
    for f in fringe:
        if f[1] == c or f[2] == c:
            if f[1] == other or f[2] == other:
                return True

    return False

def isInDistanceFringe(c, fringe):
    # checks if a distance is in the fringe
    for f in fringe:
        if f[1] == c:
            return True

    return False

def updateAccessibilityFringe(cave, fringe):
    # adds connections to the accessibility fringe
    for i in range(len(fringe)):
        fringe[i] = (cave.getNumDualConnections(fringe[i][1], fringe[i][2]), fringe[i][1], fringe[i][2])

    fringe = sorted(fringe, key=operator.itemgetter(0))

def getRandomMinFromAccessibilityFringe(fringe):
    # returns a random connection from the fringe
    # of the lowest possible distance
    fringe = sorted(fringe, key=operator.itemgetter(0))
    minVal = 100000000000
    for f in fringe:
        if f[0] <= minVal:
            minVal = f[0]

    options = [f for f in fringe if f[0] == minVal]

    returnVal = random.choice(options)
    return fringe.pop(fringe.index(returnVal))

def areAllAccessible(cave):
    # checks if all of the caverns are accessible
    # end check

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
    # adds in connections randomly, while adhering to the rules
    for i in range(iterations):
        # make connections if possible
        current = cave.getRandomCavern()
        other = random.choice(cave.getAdjacent(current))

        if len(cave.getConnections(current)) < 3 and len(cave.getConnections(other)) < 3:
            cave.addConnection(current, other)