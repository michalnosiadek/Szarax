import pygame

TILE_SIZE = 20
SNAKE_COLOR = (0, 255, 100)


class Szarax:
    def __init__(self, x, y):
        self.body = [(x, y)]
        self.length = 1
        self.direction = (0, -1)
        self.next_direction = self.direction
        self.hit_count = 0
        self.score = 0

    def move(self):
        if (self.next_direction[0] * -1, self.next_direction[1] * -1) != self.direction:
            self.direction = self.next_direction

        head = self.body[0]
        new_head = (
            head[0] + self.direction[0] * TILE_SIZE,
            head[1] + self.direction[1] * TILE_SIZE,
        )

        # Wall bounce
        new_head = (
            max(0, min(new_head[0], TILE_SIZE * 47)),
            max(0, min(new_head[1], TILE_SIZE * 23)),
        )

        self.body.insert(0, new_head)
        if len(self.body) > self.length:
            self.body.pop()

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, SNAKE_COLOR, (*segment, TILE_SIZE, TILE_SIZE))

    def set_direction(self, dx, dy):
        self.next_direction = (dx, dy)

    def head_pos(self):
        return self.body[0]

    def grow(self):
        self.length += 1
        self.score += 1

    def hit(self):
        self.hit_count += 1
