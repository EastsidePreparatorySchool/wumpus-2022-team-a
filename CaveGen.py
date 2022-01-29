import random

def makeAllAccessible(cave, hazards):
    current = 0
    fringe = []
    visited = []

    for c in cave.getAdjacent(current):
        if not isInAccessibilityFringe(c, fringe) and c not in visited and c not in hazards:
            fringe.append((current, c))

    while fringe:
        # get new node
        newConnection = fringe.pop()
        current = newConnection[0]
        other = newConnection[1]
        if current not in visited: visited.append(current)

        # if not too many connections
        if len(cave.getConnections(other)) < 3 and len(cave.getConnections(current)) < 3:
            # add connection
            cave.addConnection(other, current)
            if other not in visited: visited.append(other)

        # add neighbors to fringe
        for c in cave.getAdjacent(other):
            if not isInAccessibilityFringe(c, fringe) and c not in visited and c not in hazards:
                fringe.append((other, c))

    # make connections to each of the hazards
    for h in hazards:
        other = random.choice(cave.getAdjacent(h))
        if len(cave.getConnections(h)) < 3 and len(cave.getConnections(other)) < 3:
            cave.addConnection(h, other)

def isInAccessibilityFringe(c, fringe):
    for f in fringe:
        if f[0] == c or f[0] == c:
            return True

    return False

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
    return len(accessible) >= 30, accessible
        
    
def makeMoreConnections(cave, iterations):
    for i in range(iterations):
        # make connections if possible
        randRow = random.choice(cave.caverns)
        current = random.choice(randRow)
        other = random.choice(cave.getAdjacent(current))

        if len(cave.getConnections(current)) < 3 and len(cave.getConnections(other)) < 3:
            cave.addConnection(current, other)