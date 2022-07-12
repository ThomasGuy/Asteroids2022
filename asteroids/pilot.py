# players ship physics

import math
import pyglet
from pyglet.window import key
from pyglet.sprite import Sprite
from .physical_object import PhysicalObject
from .missile import Missile
from .helper import angle_to_vector
from .resources import get_image, get_info, pyglet_sound


class Pilot(PhysicalObject):
    """
    Here we use a sub sub class of Sprite. We need to make this class an
    event handler in 'Version3'.
    """

    def __init__(self, dimension, *args, **kwargs):
        super().__init__(
            img=get_image("engine_stop"), info=get_info("engine_stop"), *args, **kwargs
        )
        self.player = pyglet.media.Player()
        self.dimension = dimension
        # Tell the game handler about any event handlers
        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]
        # constants to adjust
        self.thrust = 300.0
        self.rotate_speed = 200.0
        self.friction = 1.0
        # Create a child sprite to show when ship is thrusting
        self.ship_engine = Sprite(img=get_image("engine_thrust"), *args, **kwargs)
        self.ship_engine.scale = 0.75
        self.ship_engine.visible = False
        # New missiles to add to game_objects
        self.new_missiles = set()
        self.sound = pyglet_sound("thrust_sound")

    def update(self, dt):
        """
        We need to call PhysicalObject‘s update() method and then respond to
        input
        """
        super().update(dt)
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction

        if self.key_handler[key.LEFT] or self.key_handler[key.A]:
            self.rotation -= self.rotate_speed * dt
        if self.key_handler[key.RIGHT] or self.key_handler[key.D]:
            self.rotation += self.rotate_speed * dt
        if self.key_handler[key.UP] or self.key_handler[key.W]:
            vector = angle_to_vector(-math.radians(self.rotation))
            self.velocity_x += vector[0] * self.thrust * dt
            self.velocity_y += vector[1] * self.thrust * dt
            self.ship_engine.rotation = self.rotation
            self.ship_engine.x = self.x
            self.ship_engine.y = self.y
            self.ship_engine.visible = True
            # self.sound.rewind()
            self.player.queue(self.sound)
            self.player.play()
        else:
            self.ship_engine.visible = False
            self.player.seek(0.0)

        if self.enemy:
            if self.key_handler[key.SPACE]:
                self.fire()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.fire()

    def fire(self):
        vector = angle_to_vector(-math.radians(self.rotation))
        missile_x = self.x + vector[0] * self.radius
        missile_y = self.y + vector[1] * self.radius
        new_missile = Missile(
            x=missile_x,
            y=missile_y,
            batch=self.batch,
            dimension=self.dimension,
            img=get_image("missile"),
            info=get_info("missile"),
            sound=pyglet_sound("missile_sound"),
        )
        new_missile.velocity_x = self.velocity_x + vector[0] * new_missile.speed
        new_missile.velocity_y = self.velocity_y + vector[1] * new_missile.speed
        self.new_missiles.add(new_missile)

    def delete(self):
        self.player.seek(0.0)
        self.ship_engine.delete()
        super().delete()
