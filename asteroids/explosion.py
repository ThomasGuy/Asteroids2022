__author__ = "Tom Guy"

import random
from .physical_object import PhysicalObject
from .resources import effect_anims, get_info, get_sound


class Explosion(PhysicalObject):
    def __init__(self, *args, **kwargs):
        boom = random.choice([0, 1, 2, 3])
        super().__init__(
            img=effect_anims[boom], info=get_info("explosion"), *args, **kwargs
        )
        self.sound = get_sound("explosion_sound")
        self.x -= self.center[0]
        self.y -= self.center[1]
        self.sound.play()

    def on_animation_end(self):
        self.delete()
        self.sound.stop()
