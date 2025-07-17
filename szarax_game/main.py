import pygame
import sys
import random
from storm import Storm
from szarax import Szarax
from rock import Rock
from star import Star

TILE_SIZE = 20
BOARD_WIDTH = 48
BOARD_HEIGHT = 24
WINDOW_WIDTH = TILE_SIZE * BOARD_WIDTH
WINDOW_HEIGHT = TILE_SIZE * BOARD_HEIGHT
FPS = 10

DARK_BLUE = (10, 10, 30)
WHITE = (255, 255, 255)
RED = (255, 50, 50)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Szarax z Gór Gwieździstych")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 20)

pygame.mixer.music.load("assets/ambient_river.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

szarax = Szarax(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
rocks = []
stars = [Star()]
frame_count = 0
storm = Storm()


def draw_ui():
    text = f"Gwiazdy: {szarax.score}/7  Trafienia: {szarax.hit_count}/3"
    label = font.render(text, True, WHITE)
    screen.blit(label, (10, 5))


def check_collision(obj1_pos, obj2_pos):
    return obj1_pos[0] == obj2_pos[0] and obj1_pos[1] == obj2_pos[1]


def end_screen(message):
    screen.fill(DARK_BLUE)
    label = font.render(message, True, RED)
    screen.blit(label, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2))
    dark_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    dark_surface.fill((0, 0, 0, 200))

    light_radius = TILE_SIZE * 3
    head_x, head_y = szarax.head_pos()
    pygame.draw.circle(
        dark_surface,
        (0, 0, 0, 0),
        (head_x + TILE_SIZE // 2, head_y + TILE_SIZE // 2),
        light_radius,
    )

    screen.blit(dark_surface, (0, 0))

    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


while True:
    screen.fill(DARK_BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        szarax.set_direction(0, -1)
    elif keys[pygame.K_DOWN]:
        szarax.set_direction(0, 1)
    elif keys[pygame.K_LEFT]:
        szarax.set_direction(-1, 0)
    elif keys[pygame.K_RIGHT]:
        szarax.set_direction(1, 0)

    szarax.move()

    storm.update(frame_count, szarax.score)
    storm.draw(screen)

    if frame_count % 30 == 0 and len(stars) < 3:
        stars.append(Star())

    if frame_count % 10 == 0:
        rocks.append(Rock())

    for star in stars[:]:
        star.update()
        star.draw(screen)
        if check_collision(star.get_pos(), szarax.head_pos()):
            szarax.grow()
            stars.remove(star)
        elif star.is_expired():
            stars.remove(star)

    for rock in rocks[:]:
        rock.update()
        rock.draw(screen)
        if check_collision(rock.get_pos(), szarax.head_pos()):
            szarax.hit()
            rocks.remove(rock)
        elif rock.y < 0:
            rocks.remove(rock)
        if storm.check_strike_hit(szarax.head_pos()):
            szarax.hit()

    szarax.draw(screen)
    draw_ui()

    if szarax.hit_count >= 3:
        end_screen("Przegrałeś! Szarax został pokonany...")
    elif szarax.score >= 7:
        end_screen("Wygrałeś! Szarax rozświetlił rzekę!")

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1
