# Asteroid class

import random
from .physical_object import PhysicalObject


class Asteroid(PhysicalObject):
    """An asteroid that breaks up before it dies"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.angle_vel = random.random() * 300 - 150
        self.rotation = random.randint(0, 360)
        self.velocity_x = (random.random() * 2 - 1) * 80
        self.velocity_y = (random.random() * 2 - 1) * 80

    def update(self, dt):
        super().update(dt)
        self.rotation += self.angle_vel * dt

    def after_death(self):
        if self.scale > 0.25:
            num_asteroids = random.choice([2, 3, 4])
            for idx in range(num_asteroids):
                new_asteroid = Asteroid(
                    img=self.image,
                    info=self.info,
                    x=self.x,
                    y=self.y,
                    batch=self.batch,
                    dimension=self.dimension,
                )
                new_asteroid.velocity_x += self.velocity_x
                new_asteroid.velocity_y += self.velocity_y
                new_asteroid.angle_vel += self.angle_vel
                # Spawn enemy space ship
                if abs(new_asteroid.angle_vel) > 330:
                    # print('got_one %d ' % new_asteroid.angle_vel)
                    new_asteroid.enemy = True
                new_asteroid.scale = self.scale * 0.5
                new_asteroid.radius *= 0.5
                self.new_objects.add(new_asteroid)
