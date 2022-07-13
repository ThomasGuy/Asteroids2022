""" start Asteroids """

__author__ = "Tom Guy 2016"

import sys
import pyglet
from pyglet.text import Label

from asteroids import (
    State,
    Explosion,
    Asteroid,
    group_collide,
    group_group_collide,
    pyglet_sounds,
)

music = pyglet_sounds["sound_track"]

# Set display for full_screen mode
display = pyglet.canvas.Display()
screen = display.get_screens()
game_window = pyglet.window.Window(fullscreen=True, screen=screen[1])
# game_window = pyglet.window.Window(1200, 900)
game_window.set_mouse_visible(False)
main_batch = pyglet.graphics.Batch()

PLAYER = pyglet.media.Player()
GAME_OVER = False
WIDTH = game_window.width
HEIGHT = game_window.height

fps_display = pyglet.window.FPSDisplay(window=game_window)

game = State(game_window)

score_label = Label(text="Score: 0", x=10, y=HEIGHT - 15, batch=main_batch)
level_label = Label(
    text="Pyglet Asteroids2 level 1",
    font_size=18,
    x=WIDTH / 2,
    y=HEIGHT - 15,
    anchor_x="center",
    batch=main_batch,
)
# Set up the game over label off screen
GAME_OVER_label = Label(
    text="GAME OVER",
    x=WIDTH / 2,
    y=-300,
    anchor_x="center",
    batch=main_batch,
    font_size=48,
)

PLAYER.queue(music)
PLAYER.play()


def reset_level():
    # Initialize game components
    game.reset_level()
    game.mk_player_ship(WIDTH / 2, HEIGHT / 2, main_batch)
    game.spawn_rocks(main_batch)
    game.player_icons(main_batch)

    # Add any specified event handlers to the event handler stack
    for obj in game.get_game_objects():
        for handler in obj.event_handlers:
            game_window.push_handlers(handler)
            game._event_stack_size += 1


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()
    fps_display.draw()


@game_window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.LCTRL:
        print("Score: %d  and level: %d" % (game._score, game.level), end="\n")
        PLAYER.pause()
        game.get_player_ship().player.pause()
        sys.exit()


def update(dt):
    global GAME_OVER, PLAYER
    level_complete = False
    ship_destroyed = False

    ##########################  Collisions  ############################
    # Missiles and Asteroids
    missiles, rocks, hits = group_group_collide(game.get_missiles(), game.get_rocks())
    # Missiles and enemy ships
    bullets, enemy, kills = group_group_collide(missiles, game.get_enemy_ship())
    game.reset_missiles(bullets)
    game.reset_enemy_ships(enemy)

    # Update score, missile and enemy_ships sets
    score_label.text = "Score: " + game.score_update(hits + kills * 10)

    # See if player ship is destroyed
    if not GAME_OVER:
        # Player_ship dies by rock
        pebbles, collision = group_collide(rocks, game.get_player_ship())
        game.reset_rocks(pebbles)
        # Player_ship dies by enemy missiles
        enemy_missiles, kill = group_collide(
            game.get_enemy_missiles(), game.get_player_ship()
        )
        game.reset_enemy_missiles(enemy_missiles)
        if kill or collision:
            ship_destroyed = True
            game.get_player_ship().sound_reset()
            game.dec_lives()

    ######################  Update game Sprites  #######################
    # extra rocks to add to game_objects
    Add_Game_Objects = set()
    # Update all Game Objects
    for obj in game.get_game_objects():
        obj.update(dt)
        Add_Game_Objects |= obj.new_objects
        obj.new_object = set()

    #####################   Remove Dead Objects  #######################
    for to_remove in [obj for obj in game.get_game_objects() if obj.dead]:
        # If any dying objects spawned any new objects, add those to
        # game_objects set later
        Add_Game_Objects |= to_remove.new_objects

        # If enemy flagged spawn enemy ship from dying asteroid. Note enemy
        # ships gets lumped in with the rocks
        if to_remove.enemy:
            game.mk_enemy_ship(main_batch)
            # Add_Game_Objects |= game.get_enemy_ship()

        # Asteroids explode
        if isinstance(to_remove, Asteroid):
            Explosion(x=to_remove.x, y=to_remove.y, batch=main_batch)

        to_remove.delete()  # Delete dead object

        # Remove dead/deleted object from the game
        game.remove_game_object(to_remove)

        # Catch the objects which expire due to old age
        if to_remove in game.get_missiles():
            game.remove_missile(to_remove)
        if to_remove in game.get_enemy_missiles():
            game.remove_enemy_missile(to_remove)
        if to_remove in game.get_enemy_ship():
            game.remove_enemy_ship(to_remove)
            to_remove.after_death()

    # Add new missiles to missile group
    game.update_all_missiles()

    # Update game objects
    Game_Objects = Add_Game_Objects.union(
        game.get_missiles(), game.get_enemy_missiles(), game.get_enemy_ship()
    )
    game.update_game_objects(Game_Objects)

    # Add newly spawned rocks to group rocks
    game.update_rocks(Add_Game_Objects)
    if len(game.get_rocks()) == 0:
        level_complete = True

    # Check for win/lose conditions
    if ship_destroyed:
        if game._num_lives > 0:
            PLAYER.seek(0.0)
            # PLAYER.queue(music)
            PLAYER.play()
            game.delete_player()
            reset_level()
        else:
            GAME_OVER_label.y = HEIGHT * 0.8
            game.clear_event_handlers()
            game.get_player_ship().pause()
            game.delete_player()
            game.player_icons(main_batch)
            GAME_OVER = True

    elif level_complete:
        game.inc_num_rocks()
        game._score += 100
        level_label.text = "Pyglet Asteroids level " + str(game.level)
        reset_level()


if __name__ == "__main__":
    reset_level()
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
