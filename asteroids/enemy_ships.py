__author__ = "Tom Guy"

import random
import math
import pyglet

from .explosion import Explosion
from .missile import Missile
from .helper import angle_to_vector
from .physical_object import PhysicalObject
from .resources import get_image, get_sound, get_info, enemy_ship


class EnemyShips(PhysicalObject):
    """Our enemy ship comes in doing 'loop de loop' firing missiles at
    intervals
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            img=enemy_ship["enemy"][1], info=enemy_ship["enemy"][0], *args, **kwargs
        )

        self.speed = 200  # random.choice([250, 350, 450])
        pyglet.clock.schedule_once(self.die, 7)
        pyglet.clock.schedule_interval(self.fire, 0.5)
        self.new_missiles = set()

    def fire(self, dt):
        vector = angle_to_vector(random.randint(0, 360))
        missile_x = self.x + vector[0] * self.radius
        missile_y = self.y + vector[1] * self.radius
        new_missile = Missile(
            x=missile_x,
            y=missile_y,
            batch=self.batch,
            dimension=self.dimension,
            img=get_image("enemy_missile"),
            info=get_info("enemy_missile"),
            sound=get_sound("missile_sound"),
        )
        new_missile.velocity_x = self.velocity_x + vector[0] * new_missile.speed
        new_missile.velocity_y = self.velocity_y + vector[1] * new_missile.speed
        self.new_missiles.add(new_missile)

    def die(self, dt):
        self.dead = True
        pyglet.clock.unschedule(self.fire)
        # self.sound.stop()

    def update(self, dt):
        """Affect course, trajectory, speed"""
        super().update(dt)
        self.velocity_x = self.speed
        self.velocity_y = self.speed * math.sin(math.radians(self.x))

    def after_death(self):
        Explosion(x=self.x, y=self.y, batch=self.batch)
        pyglet.clock.unschedule(self.fire)
