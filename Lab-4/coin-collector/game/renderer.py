"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import math

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (35, 45, 35)
COLOR_PLAYER = (80, 180, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_OBSTACLE = (200, 60, 60)
COLOR_OBSTACLE_EDGE = (120, 25, 25)
COLOR_HEART = (235, 70, 90)
COLOR_WARNING = (255, 90, 90)


def draw_scene(surface, player, coins, obstacles=(), show_player=True):
    surface.fill(COLOR_BG)
    for coin in coins:
        draw_coin(surface, coin.color, (int(coin.x), int(coin.y)), coin.radius)
    for obstacle in obstacles:
        rect = obstacle.get_rect()
        pygame.draw.rect(surface, COLOR_OBSTACLE, rect, border_radius=3)
        pygame.draw.rect(surface, COLOR_OBSTACLE_EDGE, rect, width=2, border_radius=3)
    if show_player:
        pygame.draw.rect(surface, COLOR_PLAYER, player.get_rect(), border_radius=4)


def draw_lives(surface, font, lives):
    """Lives counter in the top-right corner, drawn as red hearts."""
    label = font.render("Lives:", True, COLOR_TEXT)
    x = surface.get_width() - 10 - label.get_width() - 3 * 22
    surface.blit(label, (x, 10))
    for i in range(lives):
        cx, cy = x + label.get_width() + 14 + i * 22, 22
        pygame.draw.circle(surface, COLOR_HEART, (cx - 4, cy - 2), 5)
        pygame.draw.circle(surface, COLOR_HEART, (cx + 4, cy - 2), 5)
        pygame.draw.polygon(surface, COLOR_HEART, [(cx - 9, cy), (cx + 9, cy), (cx, cy + 9)])


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


def draw_timer(surface, font, time_left):
    """Countdown at the top centre; turns red for the last 5 seconds."""
    seconds = math.ceil(time_left)
    color = COLOR_WARNING if seconds <= 5 else COLOR_TEXT
    surf = font.render(f"Time: {seconds:2d}", True, color)
    surface.blit(surf, surf.get_rect(midtop=(surface.get_width() // 2, 10)))


_big_font = None


def draw_round_over(surface, font, reason, score):
    """Dim the play area and show why the round ended, the score, and how to restart."""
    global _big_font
    if _big_font is None:
        _big_font = pygame.font.SysFont("consolas", 44, bold=True)

    shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    shade.fill((0, 0, 0, 170))
    surface.blit(shade, (0, 0))

    cx, cy = surface.get_width() // 2, surface.get_height() // 2
    lines = [
        (font.render(reason, True, (255, 220, 80)), cy - 60),
        (_big_font.render(f"Final score: {score}", True, COLOR_TEXT), cy),
        (font.render("Press R to play again", True, (170, 220, 255)), cy + 55),
    ]
    for surf, y in lines:
        surface.blit(surf, surf.get_rect(center=(cx, y)))
