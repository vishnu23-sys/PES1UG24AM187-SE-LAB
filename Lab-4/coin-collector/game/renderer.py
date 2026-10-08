"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (35, 45, 35)
COLOR_PLAYER = (80, 180, 255)
COLOR_TEXT = (255, 255, 255)


def draw_scene(surface, player, coins):
    surface.fill(COLOR_BG)
    for coin in coins:
        draw_coin(surface, coin.color, (int(coin.x), int(coin.y)), coin.radius)
    pygame.draw.rect(surface, COLOR_PLAYER, player.get_rect(), border_radius=4)


def draw_coin(surface, color, center, radius):
    pygame.draw.circle(surface, color, center, radius)
    darker = tuple(int(c * 0.6) for c in color)
    pygame.draw.circle(surface, darker, center, radius, width=2)


def draw_coin_legend(surface, font, coin_types):
    """Bottom-left key showing each coin colour and its point value."""
    x, y = 10, surface.get_height() - 30
    for name, (value, color, _, _) in coin_types.items():
        draw_coin(surface, color, (x + 9, y + 11), 9)
        label = font.render(f"{name} {value}", True, COLOR_TEXT)
        surface.blit(label, (x + 24, y))
        x += 24 + label.get_width() + 18


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)
