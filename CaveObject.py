
from CaveGen import *
import random
import pprint

class Cave:
    # stores and manages the map of the cave
    # also loads/generates saved and new maps

    def __init__(self):
        # might not need this, try to remove if possible
        self.caverns = [[0, 1, 2, 3, 4, 5],
                        [6, 7, 8, 9, 10,11],
                        [12,13,14,15,16,17],
                        [18,19,20,21,22,23],
                        [24,25,26,27,28,29]]
        
        self.adjacencyList = {}
        for i in range(0, 30):
            # add empty array to list
            self.adjacencyList.update({i: []})

        for i in self.adjacencyList:
            if (i+1) % 6 == 0:
                # it's on the rightmost edge
                self.addAdjacent(i, i-1)
                self.addAdjacent(i, i-6)
                self.addAdjacent(i, i-5)
                self.addAdjacent(i, i+1)
                self.addAdjacent(i, i+6)
                self.addAdjacent(i, i+5)
            elif i % 6 == 0:
                # it's on the leftmost edge
                self.addAdjacent(i, i-1)
                self.addAdjacent(i, i-6)
                self.addAdjacent(i, i-5)
                self.addAdjacent(i, i+1)
                self.addAdjacent(i, i+6)
                self.addAdjacent(i, i+5)
            elif (i+1) % 2 == 0:
                # it's even
                self.addAdjacent(i, i-1)
                self.addAdjacent(i, i-6)
                self.addAdjacent(i, i+1)
                self.addAdjacent(i, i+7)
                self.addAdjacent(i, i+6)
                self.addAdjacent(i, i+5)
            else:
                # it's odd
                self.addAdjacent(i, i+1)
                self.addAdjacent(i, i+6)
                self.addAdjacent(i, i-1)
                self.addAdjacent(i, i-7)
                self.addAdjacent(i, i-6)
                self.addAdjacent(i, i-5)

        self.connectionList = {}
        for i in range(0, 30):
            # add empty array to list
            self.connectionList.update({i: []})

        self.hazards = []

    def loadPrevGame(self, gamePath):
        # loads a previous game from a path,
        # overrides the map stored here,
        # then returns the map
        
        # test code for now
        file = open(gamePath, "r")
        originalStr = file.read()
        splitStr = originalStr.split("|")[:-1]
        conList = []

        for i in range(len(splitStr)):
            commaSplitStr = splitStr[i].split(",")
            cons = []

            for i in range(len(commaSplitStr)):
                cons.append(int(commaSplitStr[i]))

            conList.append(cons)

        for i in range(len(conList)):
            newConList = []

            for item in conList[i]:
                newConList.append(item)

            self.connectionList[i] = newConList
        file.close()

        return self.caverns, self.adjacencyList, self.connectionList

    def saveMapFile(self, path):
        # saves a files with the information stored in the map
        file = open(path, "w")

        for item in self.connectionList:
            string = ""
            connections = self.connectionList[item]
            for i in range(len(connections)):
                con = connections[i]
                string = string + str(con)
                if (i != len(connections)-1):
                    string = string + ","
            
            string = string + "|"
            file.write(string)

        file.close()

    def loadPresetMap(self, num):
        if type(num) is int:
            return self.loadPrevGame("MapFiles/test" + str(num) + ".txt")
        else:
            print("invalid input:", num)
            return -1

    def genNewMap(self, hazards):
        # generates a new map using a randomized algorithm
        # overriding the map stored here,
        # then returns the map

        self.importHazards(hazards)

        makeAllAccessible(self, self.hazards)
        makeMoreConnections(self, 15)

        return self.caverns, self.adjacencyList, self.connectionList

    def getAdjacent(self, cavern):
        # returns the adjacent caverns of a certain cavern
        return self.adjacencyList[cavern]

    def getRandomCavern(self):
        # returns a random cavern
        randRow = random.choice(self.caverns)
        return random.choice(randRow)

    def getDist(self, cav1, cav2):
        # returns the distance between two given caverns
        current = cav1
        fringe = []
        visited = []

        for c in self.getConnections(current):
            if not isInDistanceFringe(c, fringe) and c not in visited:
                fringe.append((1, c))

        while fringe:
            # make fringe priority queue based on num of connections
            fringe = sorted(fringe, key=operator.itemgetter(0))

            # get new node
            newConnection = fringe.pop(0)
            cost = newConnection[0]
            current = newConnection[1]
            if current not in visited: visited.append(current)

            # if it has found the correct cavern
            if current == cav2:
                # goal check completed
                return cost

            # add neighbors to fringe
            for c in self.getConnections(current):
                if not isInDistanceFringe(c, fringe) and c not in visited:
                    fringe.append((cost+1, c))

    def isAccessible(self, cavern):
        # returns whether or not a cavern is accessible 
        # with current connection configuration
        if cavern == 0: return True
        current = cavern
        visited = []
        run = True
        while(run):
            if self.getConnections(current):
                next_cav = min(self.getConnections(current))
                
                
                visited.append(current)
                current = next_cav
                if current == 0:
                    run = False
                    return True
            else:
                run = False
                return False

    def areAdjacent(self, cav1, cav2):
        # returns if two caverns are adjacent or not
        return cav2 in self.getAdjacent(cav1)

    def getConnections(self, cavern):

        # returns the caverns connected to a certain cavern
        return self.connectionList[cavern]
    
    def getNumDualConnections(self, cav1, cav2):
        # returns the number of total connections for two caverns
        return len(self.getConnections(cav1)) + len(self.getConnections(cav2))

    def importHazards(self, haz):
        # imports hazards into list for use in cave generation
        self.hazards = []

        for i in range(30):
            print(i)
            if haz[i] != "":
                self.hazards.append(i)
    
    def addAdjacent(self, index, addIndex):
        # adds a reference of an adjacent cavern for a given cavern
        idx = addIndex % 30
        
        # if it's not already in there, add it
        if idx not in self.adjacencyList[index]:
            self.adjacencyList[index].append(idx)

    def addConnection(self, caveNum1, caveNum2):
        # adds a connection between two caverns
        if caveNum1 not in self.connectionList[caveNum2] and caveNum2 not in self.connectionList[caveNum1]:
            self.connectionList[caveNum1].append(caveNum2)
            self.connectionList[caveNum2].append(caveNum1)

    def printSelf(self):
        # prints the connections and adjacent caverns
        pprint.pprint(self.adjacencyList)
        pprint.pprint(self.connectionList)

# cave = Cave()

# cave.loadPresetMap(10)
# cave.printSelf()