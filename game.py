import os
import pygame
import pacman

# import image2gif
from pygame.locals import *
from random import randint

# Grid properties
CELL_WIDTH = 70
CELL_HEIGHT = 70
CELL_MARGIN = 0

GRID_WIDTH = 10
GRID_HEIGHT = 10

# PACMAN = 0
EMPTY = 1
WALL = 2
GREEN_COIN = 3
BLUE_COIN = 4
YELLOW_COIN = 5

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (76, 175, 80)
BLUE = (33, 150, 243)
YELLOW = (253, 216, 53)

# grid = []
# for row in range(10):
#     grid.append([])
#     for column in range(10):
#         grid[row].append(randint(1,5))

# grid[0][0] = PACMAN


width = (CELL_WIDTH * GRID_WIDTH) + (CELL_MARGIN * (GRID_WIDTH - 1))
height = (CELL_HEIGHT * GRID_HEIGHT) + (CELL_MARGIN * (GRID_HEIGHT - 1)) + 250
screenshots = []


def main():
    game_over = False

    clock = pygame.time.Clock()
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('PacFix')
    pygame.mouse.set_visible(0)

    screen.fill(WHITE)

    pacman_close = pygame.image.load('pacman/pacman-close.png')
    pacman_open = pygame.image.load('pacman/pacman-open.png')
    g_coin = pygame.image.load('pacman/coin-green.png')
    b_coin = pygame.image.load('pacman/coin-blue.png')
    y_coin = pygame.image.load('pacman/coin-yellow.png')
    wl = pygame.image.load('pacman/wall.png')

    mouth_open = False
    frame = 60



    coin_values = []
    v = pacman.setColorValue()
    coin_values.append(v)
    count = 0
    time = 60
    while not game_over:

        screen.fill(WHITE)
        clock.tick(60)
        frame -= 1
        if frame == 0:
            frame = 60
            mouth_open = not mouth_open
            pacman.loop()
            count += 1
            if count == 5:
                v = pacman.setColorValue()
                coin_values.append(v)
                count = 0
            time -= 1

            # filename = 'screenshot{}.jpg'.format(len(screenshots))
            # screenshots.append(filename)
            # pygame.image.save(screen, filename)

        for column in range(10):
            for row in range(10):
                value = pacman.BOARD[row][column].entity
                pos = [row*CELL_WIDTH, column*CELL_HEIGHT]
                if isinstance(value, pacman.PacMan):
                    pos[0] += 10
                    pos[1] += 10
                    if mouth_open:
                        screen.blit(pacman_open, tuple(pos))
                    else:
                        screen.blit(pacman_close, tuple(pos))
                elif isinstance(value, pacman.Wall):
                    screen.blit(wl, tuple(pos))
                elif isinstance(value, pacman.Coin):
                    pos[0] += 25
                    pos[1] += 25
                    if value.color == 0:
                        screen.blit(g_coin, tuple(pos))
                    elif value.color == 1:
                        screen.blit(b_coin, tuple(pos))
                    elif value.color == 2:
                        screen.blit(y_coin, tuple(pos))
                elif value is None:
                    pygame.draw.rect(screen,
                                     WHITE,
                                     [(CELL_MARGIN + CELL_WIDTH) * row + CELL_MARGIN,
                                      (CELL_MARGIN + CELL_HEIGHT) * column + CELL_MARGIN,
                                      CELL_WIDTH,
                                      CELL_HEIGHT])

        # coin values

        if len(coin_values) > 1:
            interval = width / (len(coin_values) - 1)

            for i, coins in enumerate(coin_values):
                green = get_graph_point(interval * i, coins[0])
                blue = get_graph_point(interval * i, coins[1])
                yellow = get_graph_point(interval * i, coins[2])

                pygame.draw.circle(screen, GREEN, green, 2)
                pygame.draw.circle(screen, BLUE, blue, 2)
                pygame.draw.circle(screen, YELLOW, yellow, 2)

                if i > 0:
                    start = get_graph_point(interval * i, coins[0])
                    end = get_graph_point(interval * (i - 1), coin_values[i - 1][0])
                    pygame.draw.line(screen, GREEN, start, end)

                    start = get_graph_point(interval * i, coins[1])
                    end = get_graph_point(interval * (i - 1), coin_values[i - 1][1])
                    pygame.draw.line(screen, BLUE, start, end)

                    start = get_graph_point(interval * i, coins[2])
                    end = get_graph_point(interval * (i - 1), coin_values[i - 1][2])
                    pygame.draw.line(screen, YELLOW, start, end)

        font = pygame.font.SysFont('monospace', 15)
        pygame.draw.line(screen, BLACK, (0, 700), (700, 700))
        screen.blit(g_coin, (250, 720))
        label_green = font.render('= {}'.format(coin_values[-1][0]), 1, BLACK)
        screen.blit(label_green, (275, 722))

        screen.blit(b_coin, (350, 720))
        label_blue = font.render('= {}'.format(coin_values[-1][1]), 1, BLACK)
        screen.blit(label_blue, (375, 722))

        screen.blit(y_coin, (450, 720))
        label_yellow = font.render('= {}'.format(coin_values[-1][2]), 1, BLACK)
        screen.blit(label_yellow, (475, 722))

        label_points = font.render('points = {}'.format(pacman.PACMAN.points), 1, BLACK)
        screen.blit(label_points, (350, 750))

        label_time = font.render('time: {}'.format(time), 1, BLACK)
        screen.blit(label_time, (150, 750))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pacman.PACMAN.direction = 'down'
                if event.key == pygame.K_RIGHT:
                    pacman.PACMAN.direction = 'right'
                if event.key == pygame.K_LEFT:
                    pacman.PACMAN.direction = 'left'
                if event.key == pygame.K_UP:
                    pacman.PACMAN.direction = 'up'


        if time < 1:
            screen.fill(BLACK)
            label = font.render('SCORE: {}'.format(pacman.PACMAN.points), 1, WHITE)
            screen.blit(label, (width/2, height/2))
            # from PIL import Image
            # s = [Image.open(s) for s in screenshots]
            # image2gif.writeGif("replay.gif", s)


        pygame.display.flip()
            # game_over = True




def get_graph_point(x, y):
    y = height - 100 - y * 10
    return (x, y)


if __name__ == '__main__': main()
