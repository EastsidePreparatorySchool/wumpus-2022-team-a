class Cave:
    # stores and manages the map of the cave
    # also loads/generates saved and new maps

    def __init__():
        self.caverns = []

    def load_prev_game(game_path):
        # loads a previous game from a path, 
        # overrides the map stored here, 
        # then returns the map
        return self.caverns

    def load_preset_map(map_num):
        # loads a preset, built-in map,
        # overrides the map stored here,
        # then returns the map
        return self.caverns

    def gen_new_map(settings):
        # generates a new map using a randomized algorithm
        # overriding the map stored here,
        # then returns the map
        return self.caverns

    def get_current_map():
        # returns the current map
        return self.caverns

    def get_adjacent(cavern):
        # returns the adjacent caverns of a certain cavern
        return None

    def get_connected(cavern):
        # returns the caverns connected to a certain cavern
        return None