# the sprite movement class

import pyglet
from .helper import distance


class PhysicalObject(pyglet.sprite.Sprite):
    """
    subclass of Sprite, here assign velocity and update position
    """
    def __init__(self, info=None, sound=None, dimension=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dimension = dimension
        self.dead = False
        self.enemy = False
        self.angle_vel = 0
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.info = info
        self.radius = info.get_radius()
        self.center = info.get_center()
        self.animated = info.get_animated
        self.new_objects = set()
        self.sound = sound
        # Tell the game handler about any event handlers
        # Only applies to things with keyboard/mouse input
        self.event_handlers = []

    def __str__(self):
        type(self)

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()

    def check_bounds(self):
        min_x = -self.radius
        min_y = -self.radius
        max_x = self.dimension[0] + self.radius
        max_y = self.dimension[1] + self.radius
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

    def collide(self, another):
        separation = distance(self.position, another.position)
        return separation <= self.radius + another.radius
