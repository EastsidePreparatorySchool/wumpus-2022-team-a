# this module has the main game objects, other than control, to be accessed by the game files

from GameLocations import GameLocations
from CaveObject import Cave
from Player import Player
from LazyWumpusObject import LazyWumpus
from Trivia import Trivia
from HighScoresObject import HighScores
from Sound import Sound


player = Player()
print("Player initialized")

wumpus = LazyWumpus()
print("Wumpus initialized")

cave = Cave()
print("Cave initialized")

location = GameLocations()
print("Location initialized")
# location.spawnItems(wumpus, cave, player)

trivia = Trivia()
print("Trivia initialized")

highScores = HighScores()
print("Highscores initialized")

sound = Sound(True)
print("Sound initialized")