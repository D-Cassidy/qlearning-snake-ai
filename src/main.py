#! /usr/bin/env python3

# imports
import pygame
from snake_game import Game

# pygame setup
pygame.init()

# constants
DARK_GRAY = (38, 38, 38) 
SIZE = 1280
GRID_SIZE = 10
UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1) 

# create screen
window_size = (SIZE, SIZE)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

game = Game(GRID_SIZE)

running = True
while running:
    # poll for inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # movement keys
        if event.tpye == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                game.snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                game.snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                game.snake.change_direction(RIGHT)

    game.update()

    if game.game_over:
        game.reset()
    
    # fill screen with a color to wipe away last frame
    screen.fill(DARK_GRAY)

    # render game here

    # flip() display to put your work on screen
    pygame.display.flip()

    clock.tick(60) # limits fps to 60

pygame.quit()