"""
Coin: a static collectible circle. Drawn as a circle, hit-tested as a
bounding square around it.

Three coin types exist, each with its own value, colour and size so they
are easy to tell apart. Rarer coins are worth more.
"""

import random

import pygame

# name: (value, colour, radius, spawn weight)
COIN_TYPES = {
    "bronze": (1, (205, 127, 50), 10, 60),
    "silver": (3, (200, 205, 215), 12, 30),
    "gold": (5, (255, 210, 40), 14, 10),
}


def random_coin_type():
    names = list(COIN_TYPES)
    weights = [COIN_TYPES[n][3] for n in names]
    return random.choices(names, weights=weights)[0]


class Coin:
    def __init__(self, x, y, kind="bronze"):
        value, color, radius, _ = COIN_TYPES[kind]
        self.x = x
        self.y = y
        self.kind = kind
        self.radius = radius
        self.value = value
        self.color = color

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )
