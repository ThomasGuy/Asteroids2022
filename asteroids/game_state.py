__author__ = "Tom Guy"
# 24/03/2016

###################   Version3 of Pyglet Asteroids   ###################

import random
import pygame
from pyglet.sprite import Sprite
from .asteroid import Asteroid
from .helper import distance
from .pilot import Pilot
from .enemy_ships import EnemyShips
from .resources import get_image, roids, get_info


class State:
    """Contains all game state variables
    trying not to use any globals
    """

    def __init__(self, window):
        self._game_window = window
        self._rocks = set()
        self._missiles = set()
        self._game_objects = set()
        self._enemy_ships = set()
        self._enemy_missiles = set()
        self._score = 0
        self._num_lives = 3
        self._num_rocks = 3
        self.level = 1
        self._life_icons = set()
        self._event_stack_size = 0
        # Need to pass the game_window dimensions onto each Sprite
        self.win_size = (self._game_window.width, self._game_window.height)

    # Create player ship
    def mk_player_ship(self, x, y, batch):
        self.player_ship = Pilot(x=x, y=y, batch=batch, dimension=self.win_size)
        self.player_ship.scale = 0.75
        self.player_ship.radius *= 0.75
        self._game_objects.add(self.player_ship)

    def get_player_ship(self):
        return self.player_ship

    def delete_player(self):
        self.remove_game_object(self.player_ship)
        self.player_ship.delete()

    # Create enemy ship
    def mk_enemy_ship(self, batch):
        enemy_x = -10
        enemy_y = self.player_ship.y + self.win_size[1] * 0.4
        enemy_ship = EnemyShips(
            x=enemy_x, y=enemy_y, batch=batch, dimension=self.win_size
        )
        self._enemy_ships.add(enemy_ship)

    def get_enemy_ship(self):
        return self._enemy_ships

    def reset_enemy_ships(self, new_enemy_set):
        self._enemy_ships = new_enemy_set

    def remove_enemy_ship(self, obj):
        self._enemy_ships.remove(obj)

    def enemy_delete(self):
        for enemy in self.enemy_ships:
            if enemy.dead:
                enemy.delete()

    # Set of rocks
    def get_rocks(self):
        return self._rocks

    def reset_rocks(self, new_rocks_set):
        self._rocks = new_rocks_set

    def update_rocks(self, more_rocks):
        self._rocks |= more_rocks

    # Set of missiles
    def get_missiles(self):
        return self._missiles

    def reset_missiles(self, new_missile_set):
        self._missiles = new_missile_set

    def update_all_missiles(self):
        for enemy in self._enemy_ships:
            self._enemy_missiles |= enemy.new_missiles
            enemy.new_missiles = set()
        if self.player_ship:
            self._missiles |= self.player_ship.new_missiles
            self.player_ship.new_missiles = set()

    def remove_missile(self, missile):
        self._missiles.remove(missile)

    # Set of enemy missiles
    def get_enemy_missiles(self):
        return self._enemy_missiles

    def remove_enemy_missile(self, missile):
        self._enemy_missiles.remove(missile)

    def reset_enemy_missiles(self, new_missile_set):
        self._enemy_missiles = new_missile_set

    # Set of all game_objects
    def get_game_objects(self):
        return self._game_objects

    def update_game_objects(self, more):
        self._game_objects |= more

    def remove_game_object(self, obj):
        self._game_objects.remove(obj)

    # Current score
    def score_update(self, hits):
        self._score += hits * 10
        return str(self._score)

    # Lives left
    def dec_lives(self):
        self._num_lives -= 1

    # Number of rocks to spawn in new game level
    def inc_num_rocks(self):
        self._num_rocks += 1
        self.level += 1

    # Generate lives left icons
    def player_icons(self, batch=None):
        self._life_icons = set()
        WIDTH = self.win_size[0]
        HEIGHT = self.win_size[1]
        for idx in range(self._num_lives):
            new_sprite = Sprite(
                img=get_image("engine_stop"),
                x=WIDTH - 15 - idx * 30,
                y=HEIGHT - 15,
                batch=batch,
            )
            new_sprite.scale = 0.3
            new_sprite.rotation = -90
            self._life_icons.add(new_sprite)
        return self._life_icons

    # Spawn asteroids for each level
    def spawn_rocks(self, batch=None):
        count = 0
        while count < self._num_rocks:
            asteroid_pos = (
                random.randint(0, self.win_size[0]),
                random.randint(0, self.win_size[1]),
            )
            if distance(self.player_ship.position, asteroid_pos) > 200:
                rock = random.choice(roids)
                new_asteroid = Asteroid(
                    img=get_image(rock),
                    info=get_info(rock),
                    x=asteroid_pos[0],
                    y=asteroid_pos[1],
                    batch=batch,
                    dimension=self.win_size,
                )
                self._rocks.add(new_asteroid)
                count += 1
        self.update_game_objects(self._rocks)

    def reset_level(self):
        for obj in self._game_objects:
            obj.delete()
        for icon in self._life_icons:
            icon.delete()
        self._game_objects = set()
        self._rocks = set()
        self._missiles = set()
        self._enemy_ships = set()
        self._enemy_missiles = set()
        self.clear_event_handlers()

    # Clear the event stack of any remaining handlers from other levels
    def clear_event_handlers(self):
        while self._event_stack_size > 0:
            self._game_window.pop_handlers()
            self._event_stack_size -= 1
