import os
import time
import keyboard  # pip install keyboard

WIDTH = 48
HEIGHT = 24

player_x = WIDTH // 2
player_y = HEIGHT // 2


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def draw_board():
    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            if x == player_x and y == player_y:
                row += "@"
            else:
                row += " "
        print(row)


def get_input():
    global player_x, player_y

    if keyboard.is_pressed("up") and player_y > 0:
        player_y -= 1
    elif keyboard.is_pressed("down") and player_y < HEIGHT - 1:
        player_y += 1
    elif keyboard.is_pressed("left") and player_x > 0:
        player_x -= 1
    elif keyboard.is_pressed("right") and player_x < WIDTH - 1:
        player_x += 1


def main():
    while True:
        clear_screen()
        get_input()
        draw_board()
        time.sleep(0.05)


if __name__ == "__main__":
    main()
