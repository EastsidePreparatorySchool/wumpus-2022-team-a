import pygame

class Sound:
    def __init__(self, playMusic):
        pygame.mixer.init()

        self.coinSound = pygame.mixer.Sound('SoundFiles/coin.wav')
        self.arrowShootSound = pygame.mixer.Sound('SoundFiles/arrow_shoot.wav')
        self.arrowHitSound = pygame.mixer.Sound('SoundFiles/arrow_hit.wav')
        self.playerHitSound = pygame.mixer.Sound('SoundFiles/hit.wav')
        self.heartbeatSound = pygame.mixer.Sound('SoundFiles/heartbeat.wav')

        self.pitSound = pygame.mixer.Sound('SoundFiles/pit.wav')
        self.ambientSound1 = pygame.mixer.Sound('SoundFiles/ambient1.wav')
        self.ambientSound2 = pygame.mixer.Sound('SoundFiles/ambient2.wav')
        self.ambientSound3 = pygame.mixer.Sound('SoundFiles/ambient3.wav')

        self.batSound1 = pygame.mixer.Sound('SoundFiles/bats1.wav')
        self.batSound2 = pygame.mixer.Sound('SoundFiles/bats2.wav')
        self.wumpusSound1 = pygame.mixer.Sound('SoundFiles/wumpus1.wav')
        self.wumpusSound2 = pygame.mixer.Sound('SoundFiles/wumpus2.wav')
        self.wumpusSound3 = pygame.mixer.Sound('SoundFiles/wumpus3.wav')

        self.music = pygame.mixer.music.load('SoundFiles/music.wav')

        volumes = {"SFX": 0.1, "Ambient": 0.5, "Creatures": 0.7, "Music": 0.15}
        self.adjustSoundSettings(volumes)

        if playMusic:
            pygame.mixer.music.play(-1)

    def playSound(self, sound):
        if sound == "coin":
            self.coinSound.play()
        elif sound == "pit":
            self.pitSound.play()
        elif sound == "bat1":
            self.batSound1.play()
        elif sound == "bat2":
            self.batSound2.play()
        elif sound == "wumpus1":
            self.wumpusSound1.play()
        elif sound == "wumpus2":
            self.wumpusSound2.play()
        elif sound == "wumpus3":
            self.wumpusSound3.play()
        elif sound == "plHit":
            self.playerHitSound.play()
        elif sound == "arrHit":
            self.arrowHitSound.play()
        elif sound == "shoot":
            self.arrowShootSound.play()
        elif sound == "amb1":
            self.ambientSound1.play()
        elif sound == "amb2":
            self.ambientSound2.play()
        elif sound == "amb3":
            self.ambientSound3.play()
        elif sound == "heartbeat":
            self.heartbeatSound.play()
        else:
            print("Error! Sound of name", sound, "was not found!")

    def adjustSoundSettings(self, volumes):
        # adjusts the volumes of the sounds based on the dict of volumes given

        # SFX / Main
        self.coinSound.set_volume(volumes["SFX"])
        self.arrowShootSound.set_volume(volumes["SFX"])
        self.arrowHitSound.set_volume(volumes["SFX"])
        self.playerHitSound.set_volume(volumes["SFX"])

        # Ambient sounds
        self.pitSound.set_volume(volumes["Ambient"] * 0.25)
        self.ambientSound1.set_volume(volumes["Ambient"])
        self.ambientSound2.set_volume(volumes["Ambient"])
        self.ambientSound3.set_volume(volumes["Ambient"])

        # Sounds from creatures
        self.batSound1.set_volume(volumes["Creatures"])
        self.batSound2.set_volume(volumes["Creatures"])
        self.wumpusSound1.set_volume(volumes["Creatures"])
        self.wumpusSound2.set_volume(volumes["Creatures"])
        self.wumpusSound3.set_volume(volumes["Creatures"])

        # Music
        pygame.mixer.music.set_volume(volumes["Music"])

# pygame.init()
# sound = Sound(True)
# sound.playSound("pit")

# from time import sleep
# sleep(5)