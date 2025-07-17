import pygame
import random

TILE_SIZE = 20
CLOUD_COLOR = (60, 60, 80)
FLASH_COLOR = (255, 255, 255)


class CloudCluster:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.dx = TILE_SIZE
        self.dy = TILE_SIZE

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.left <= 0 or self.rect.right >= 48 * TILE_SIZE:
            self.dx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= 24 * TILE_SIZE:
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, CLOUD_COLOR, self.rect)

    def get_random_strike_position(self):
        x = (
            random.randint(
                self.rect.left // TILE_SIZE, (self.rect.right - TILE_SIZE) // TILE_SIZE
            )
            * TILE_SIZE
        )
        y = (
            random.randint(
                self.rect.top // TILE_SIZE + 1, (self.rect.bottom + 4) // TILE_SIZE
            )
            * TILE_SIZE
        )
        return (x, y)


class Storm:
    def __init__(self):
        self.clusters = [CloudCluster(5 * TILE_SIZE, 0, 10 * TILE_SIZE, 3 * TILE_SIZE)]
        self.flash_timer = 0
        self.strike_pos = None
        self.last_strike_frame = 0

    def update(self, frame_count, score):
        if score >= 3 and len(self.clusters) < 2:
            self.clusters.append(
                CloudCluster(30 * TILE_SIZE, 0, 10 * TILE_SIZE, 3 * TILE_SIZE)
            )
        if score >= 5 and len(self.clusters) < 3:
            self.clusters.append(
                CloudCluster(15 * TILE_SIZE, 0, 12 * TILE_SIZE, 3 * TILE_SIZE)
            )

        for cluster in self.clusters:
            cluster.move()

        if frame_count - self.last_strike_frame > 180:
            self.last_strike_frame = frame_count
            cluster = random.choice(self.clusters)
            self.strike_pos = cluster.get_random_strike_position()
            self.flash_timer = 3
            self.play_thunder()

    def draw(self, screen):
        for cluster in self.clusters:
            cluster.draw(screen)
        if self.flash_timer > 0:
            self.flash_timer -= 1
            pygame.draw.rect(
                screen, FLASH_COLOR, (*self.strike_pos, TILE_SIZE, TILE_SIZE)
            )

    def play_thunder(self):
        sound = pygame.mixer.Sound("assets/thunder.mp3")
        sound.set_volume(0.3)
        sound.play()

    def check_strike_hit(self, player_pos):
        if self.strike_pos and self.flash_timer == 2:
            return player_pos == self.strike_pos
        return False
