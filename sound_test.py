import pyglet

from pyglet.resource import media

player = pyglet.media.Player()

pyglet.resource.path = [
    "res/images/Asteroids",
    "res/images/Spaceships-KaaR",
    "res/sounds/wav",
]

pyglet.resource.reindex()

pyglet_sounds = {
    "sound_track": pyglet.media.load("res/sounds/wav/soundtrack.wav"),
    "thrust_sound": pyglet.media.StaticSource(media("space-engine-thrust.wav")),
    "explosion_sound": pyglet.media.StaticSource(
        media("explosion.wav", streaming=False)
    ),
    "missile_sound": pyglet.media.StaticSource(
        media("Laser_Shoot6.wav", streaming=False)
    ),
}


def pyglet_sound(track):
    return pyglet_sounds[track]


if __name__ == "__main__":
    test = pyglet_sound("missile_sound")
    test.play()
