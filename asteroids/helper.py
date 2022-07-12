"""Helper functions"""

import math

# helper functions to handle transformations
def angle_to_vector(ang):
    return (math.cos(ang), math.sin(ang))


def distance(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def group_collide(group, other_sprite):
    remove = set()
    collision = False
    for item in group:
        if item.collide(other_sprite):
            remove.add(item)
            item.dead = True
            collision = True
    group.difference_update(remove)
    return (group, collision)


def group_group_collide(missiles, group):
    """returns the two groups minus the dead objects"""
    remove1 = set()
    remove2 = set()
    collisions = 0
    for missile in missiles:
        for obj in group:
            if missile.collide(obj):
                collisions += 1
                missile.dead = True
                obj.dead = True
                obj.after_death()
                remove1.add(missile)
                remove2.add(obj)
    missiles.difference_update(remove1)
    group.difference_update(remove2)
    return (missiles, group, collisions)
