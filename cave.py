from CaveGen import *

class Cave:
    # stores and manages the map of the cave
    # also loads/generates saved and new maps

    def __init__(self):
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

    def loadPrevGame(self, gamePath):
        # loads a previous game from a path, 
        # overrides the map stored here, 
        # then returns the map
        return self.caverns

    def loadPresetMap(self):
        # in future, probably need preset number as a parameter

        # loads a preset, built-in map,
        # overrides the map stored here,
        # then returns the map

        self.caverns = {0, 1, 5, 6, 24, 25, 29}
        self.adjacencyList = {}
        for i in self.caverns:
            # add empty array to list
            self.adjacencyList.update({i: []})

        self.addAdjacent(0,0)
        self.addAdjacent(0,1)
        self.addAdjacent(0,5)
        self.addAdjacent(0,6)
        self.addAdjacent(0,24)
        self.addAdjacent(0,25)
        self.addAdjacent(0,29)

        self.addAdjacent(1,0)
        self.addAdjacent(1,6)

        self.addAdjacent(5,0)
        self.addAdjacent(5,6)
        self.addAdjacent(5,29)

        self.addAdjacent(6,0)
        self.addAdjacent(6,1)
        self.addAdjacent(6,5)

        self.addAdjacent(24,0)
        self.addAdjacent(24,25)
        self.addAdjacent(24,29)

        self.addAdjacent(29,0)
        self.addAdjacent(29,24)

        self.addAdjacent(25,0)
        self.addAdjacent(25,24)

        self.connectionList = {}
        for i in self.caverns:
            # add empty array to list
            self.connectionList.update({i: []})

        self.addConnection(0, 1)
        self.addConnection(0, 24)
        self.addConnection(0, 29)
        self.addConnection(1, 6)
        self.addConnection(6, 5)
        self.addConnection(29, 24)
        self.addConnection(24, 25)

        return self.caverns, self.adjacencyList, self.connectionList

    def genNewMap(self, hazards, settings):
        # generates a new map using a randomized algorithm
        # overriding the map stored here,
        # then returns the map

        makeAllAccessible(self, hazards)
        #makeMoreConnections(self, 15)

        return self.caverns, self.adjacencyList, self.connectionList

    def getAdjacent(self, cavern):
        # returns the adjacent caverns of a certain cavern
        return self.adjacencyList[cavern]

    def isAccessible(self, cavern):
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
        return cav2 in self.getAdjacent(cav1)

    def getConnections(self, cavern):
        # returns the caverns connected to a certain cavern
        return self.connectionList[cavern]
    
    def addAdjacent(self, index, addIndex):
        idx = addIndex % 30
        
        # if it's not already in there, add it
        if idx not in self.adjacencyList[index]:
            self.adjacencyList[index].append(idx)

    def addConnection(self, caveNum1, caveNum2):
        self.connectionList[caveNum1].append(caveNum2)
        self.connectionList[caveNum2].append(caveNum1)

    def printSelf(self):
        print(self.adjacencyList)
        print(self.connectionList)

        # print("1  2  3  4  5  6")
        # print("                ")
        # print("7  8  9  10 11 12")
        # print("                ")
        # print("13 14 15 16 17 18")
        # print("                ")
        # print("19 20 21 22 23 24")
        # print("                ")
        # print("25 26 27 28 29 30")

cave = Cave()
cave.genNewMap([2, 13, 22], None)
cave.printSelf()
print(areAllAccessible(cave)[0])