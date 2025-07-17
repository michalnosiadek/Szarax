import pygame
import random

TILE_SIZE = 20
ROCK_COLOR = (100, 100, 100)


class Rock:
    def __init__(self):
        self.x = random.randint(0, 47) * TILE_SIZE
        self.y = 24 * TILE_SIZE

    def update(self):
        self.y -= TILE_SIZE

    def draw(self, screen):
        pygame.draw.rect(screen, ROCK_COLOR, (self.x, self.y, TILE_SIZE, TILE_SIZE))

    def get_pos(self):
        return (self.x, self.y)
