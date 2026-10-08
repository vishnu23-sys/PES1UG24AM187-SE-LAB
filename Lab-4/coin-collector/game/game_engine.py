"""
GameEngine: owns the player, all coins and the obstacles.

Bronze, silver and gold coins (see game/coin.py) and moving obstacles,
no timer yet. Each coin is collected exactly once: `update` removes it as
soon as it is scored and spawns a new coin somewhere else.

Touching an obstacle costs one life and makes the player invulnerable
(and blink) for a short time, so a single touch is only punished once.
When the last life is lost the game stops and shows the final score.
"""

import random
import pygame

from game.player import Player
from game.coin import Coin, COIN_TYPES, random_coin_type
from game.obstacle import Obstacle
from game.collection import check_collection, check_obstacle_hit
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
NUM_OBSTACLES = 3
START_LIVES = 3
INVULNERABLE_FRAMES = 90  # 1.5 s at 60 fps
SAFE_SPAWN_DISTANCE = 140  # obstacles never start this close to the player


class GameEngine:
    def __init__(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.obstacles = [self._random_obstacle() for _ in range(NUM_OBSTACLES)]
        self.coins = [self._random_coin() for _ in range(NUM_COINS)]
        self.score = 0
        self.lives = START_LIVES
        self.invulnerable = 0
        self.game_over = False

    def _random_coin(self):
        # Don't place a coin inside an obstacle (they move, so later they
        # may still drift over one - that just makes the coin riskier).
        while True:
            x = random.randint(30, WIDTH - 30)
            y = random.randint(50, HEIGHT - 50)  # keep clear of the HUD rows
            coin = Coin(x=x, y=y, kind=random_coin_type())
            if not any(coin.get_rect().colliderect(o.get_rect().inflate(10, 10))
                       for o in self.obstacles):
                return coin

    def _random_obstacle(self):
        while True:
            w, h = random.choice([(70, 22), (22, 70), (44, 44)])
            x = random.randint(0, WIDTH - w)
            y = random.randint(0, HEIGHT - h)
            rect = pygame.Rect(x, y, w, h)
            px, py = self.player.x, self.player.y
            if (rect.centerx - px) ** 2 + (rect.centery - py) ** 2 >= SAFE_SPAWN_DISTANCE ** 2:
                vx = random.choice([-1, 1]) * random.uniform(1.0, 2.0)
                vy = random.choice([-1, 1]) * random.uniform(1.0, 2.0)
                return Obstacle(x, y, w, h, vx, vy)

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        if self.game_over:
            return

        for obstacle in self.obstacles:
            obstacle.update(WIDTH, HEIGHT)

        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.score += coin.value
            # Remove the coin so it can only be collected once, and spawn a
            # fresh one elsewhere so the play area never runs dry.
            self.coins.remove(coin)
            self.coins.append(self._random_coin())

        if self.invulnerable > 0:
            self.invulnerable -= 1
        elif check_obstacle_hit(self.player, self.obstacles):
            self.lives -= 1
            self.invulnerable = INVULNERABLE_FRAMES
            if self.lives <= 0:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        # Blink the player while invulnerable so the hit is obvious.
        show_player = (self.game_over or self.invulnerable == 0
                       or (self.invulnerable // 6) % 2 == 0)
        renderer.draw_scene(surface, self.player, self.coins, self.obstacles, show_player)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_lives(surface, font, self.lives)
        renderer.draw_coin_legend(surface, font, COIN_TYPES)
        if self.game_over:
            renderer.draw_banner(surface, font, f"Out of lives!  Final score: {self.score}")
