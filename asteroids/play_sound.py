__author__ = "Tom Guy"

import pygame

# global constants
FREQ = 22050  # same as audio CD
SIZE = -16  # unsigned 16 bit
CHANNELS = 2  # 1 == mono, 2 == stereo
BUFFER = 512  # audio buffer size in no. of samples
FRAMERATE = 30  # how often to check if playback has finished


class Sounds:
    pygame.mixer.pre_init(FREQ, SIZE, CHANNELS, BUFFER, devicename=None)
    pygame.init()

    def __init__(self, track, streaming=False, volume=0.5):
        self.track = track
        self.volume = volume
        self.streaming = streaming
        if not streaming:
            self.sound = pygame.mixer.Sound(self.track)
        else:
            self.playmusic(self.track)

    def play(self):
        self.sound.set_volume(self.volume)
        self.sound.play()

    def stop(self):
        self.sound.stop()

    def fadeout(self):
        self.sound.fadeout(400)

    def playmusic(self, soundfile):
        """
        Stream music with mixer.music module in blocking manner.
        This will stream the sound from disk while playing.
        """
        clock = pygame.time.Clock()
        pygame.mixer.music.load(soundfile)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(FRAMERATE)
