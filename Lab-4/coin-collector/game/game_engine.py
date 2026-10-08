"""
GameEngine: owns the player, all coins and the obstacles.

Bronze, silver and gold coins (see game/coin.py), moving obstacles and
a 30-second timed round. Each coin is collected exactly once: `update`
removes it as soon as it is scored and spawns a new coin somewhere else.

Touching an obstacle costs one life and makes the player invulnerable
(and blink) for a short time, so a single touch is only punished once.
The round ends when the timer reaches zero or the last life is lost,
whichever comes first; the final score is shown and R starts a new round
with score, lives and timer reset.
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
ROUND_SECONDS = 30
SAFE_SPAWN_DISTANCE = 140  # obstacles never start this close to the player


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Start a fresh round: new layout, score, lives and timer."""
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.obstacles = [self._random_obstacle() for _ in range(NUM_OBSTACLES)]
        self.coins = [self._random_coin() for _ in range(NUM_COINS)]
        self.score = 0
        self.lives = START_LIVES
        self.invulnerable = 0
        self.time_left = float(ROUND_SECONDS)
        self.round_over = False
        self.end_reason = ""

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

    def handle_event(self, event):
        if self.round_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset()

    def handle_input(self, keys_pressed):
        if self.round_over:
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

    def update(self, dt):
        if self.round_over:
            return

        self.time_left -= dt
        if self.time_left <= 0:
            self._end_round("Time's up!")
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
                self._end_round("Out of lives!")

    def _end_round(self, reason):
        self.time_left = max(0.0, self.time_left)
        self.round_over = True
        self.end_reason = reason

    def draw(self, surface, font):
        from game import renderer
        # Blink the player while invulnerable so the hit is obvious.
        show_player = (self.round_over or self.invulnerable == 0
                       or (self.invulnerable // 6) % 2 == 0)
        renderer.draw_scene(surface, self.player, self.coins, self.obstacles, show_player)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_timer(surface, font, self.time_left)
        renderer.draw_lives(surface, font, self.lives)
        renderer.draw_coin_legend(surface, font, COIN_TYPES)
        if self.round_over:
            renderer.draw_round_over(surface, font, self.end_reason, self.score)
