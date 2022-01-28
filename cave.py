class Cave:
    # stores and manages the map of the cave
    # also loads/generates saved and new maps

    def __init__(self):
        self.caverns = [[0, 1, 2, 3, 4, 5],
                        [6, 7, 8, 9, 10,11],
                        [12,13,14,15,16,17],
                        [18,19,20,21,22,23],
                        [24,25,26,27,28,29]]
        
        self.adjacency_list = {}
        for i in range(0, 30):
            # add empty array to list
            self.adjacency_list.update({i: []})

        for i in self.adjacency_list:
            if (i+1) % 6 == 0:
                # it's on the rightmost edge
                self.add_adjacent(i, i-1)
                self.add_adjacent(i, i-6)
                self.add_adjacent(i, i-5)
                self.add_adjacent(i, i+1)
                self.add_adjacent(i, i+6)
                self.add_adjacent(i, i+5)
            elif i % 6 == 0:
                # it's on the leftmost edge
                self.add_adjacent(i, i-1)
                self.add_adjacent(i, i-6)
                self.add_adjacent(i, i-5)
                self.add_adjacent(i, i+1)
                self.add_adjacent(i, i+6)
                self.add_adjacent(i, i+5)
            elif (i+1) % 2 == 0:
                # it's even
                self.add_adjacent(i, i-1)
                self.add_adjacent(i, i-6)
                self.add_adjacent(i, i+1)
                self.add_adjacent(i, i+7)
                self.add_adjacent(i, i+6)
                self.add_adjacent(i, i+5)
            else:
                # it's odd
                self.add_adjacent(i, i+1)
                self.add_adjacent(i, i+6)
                self.add_adjacent(i, i-1)
                self.add_adjacent(i, i-7)
                self.add_adjacent(i, i-6)
                self.add_adjacent(i, i-5)

        self.connection_list = {}
        for i in range(0, 30):
            # add empty array to list
            self.adjacency_list.update({i: []})

    def load_prev_game(self, game_path):
        # loads a previous game from a path, 
        # overrides the map stored here, 
        # then returns the map
        return self.caverns

    def load_preset_map(self, map_num):
        # loads a preset, built-in map,
        # overrides the map stored here,
        # then returns the map
        return self.caverns

    def gen_new_map(self, settings):
        # generates a new map using a randomized algorithm
        # overriding the map stored here,
        # then returns the map
        return self.caverns

    def get_current_map(self):
        # returns the current map
        return self.caverns, self.adjacency_list, self.connection_list

    def get_adjacent(self, cavern):
        # returns the adjacent caverns of a certain cavern
        return self.adjacency_list.get(cavern)

    def get_connected(self, cavern):
        # returns the caverns connected to a certain cavern
        return self.connection_list.get(cavern)
    
    def add_adjacent(self, index, addIndex):
        idx = addIndex % 30
        
        # if it's not already in there, add it
        if idx not in self.adjacency_list[index]:
            self.adjacency_list[index].append(idx)

cave = Cave()