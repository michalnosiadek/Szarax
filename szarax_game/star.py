import pygame
import random

TILE_SIZE = 20
STAR_COLOR = (255, 255, 150)


class Star:
    def __init__(self):
        self.x = random.randint(0, 47) * TILE_SIZE
        self.y = random.randint(4, 23) * TILE_SIZE
        self.timer = random.randint(30, 60)

    def update(self):
        self.timer -= 1

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            STAR_COLOR,
            (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2),
            TILE_SIZE // 3,
        )

    def is_expired(self):
        return self.timer <= 0

    def get_pos(self):
        return (self.x, self.y)
