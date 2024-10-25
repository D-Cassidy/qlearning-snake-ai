#! /usr/bin/env python3

# imports
import pygame
from snake_game import Game

# pygame setup
pygame.init()

# colors
BACKGROUND_COLOR = (38, 38, 38)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)

# constants
SIZE = 1280
GRID_SIZE = (30, 30)
UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1) 

# create pygame screen
window_size = (SIZE, SIZE)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

# initialize game
game = Game(GRID_SIZE, window_size)

running = True
while running:
    # poll for inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # movement keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.snake.change_direction(UP)
            elif event.key == pygame.K_DOWN:
                game.snake.change_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                game.snake.change_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                game.snake.change_direction(RIGHT)

    # update game
    game.update()

    # check for game over
    if game.game_over:
        game.reset()
    
    # fill screen with a color to wipe away last frame
    screen.fill(BACKGROUND_COLOR)

    # RENDER GAME
    # draw snake
    for segment in game.snake.body:
        segment_rect = pygame.Rect(segment[1] * GRID_SIZE[0],
                                   segment[0] * GRID_SIZE[1],
                                   GRID_SIZE[0], GRID_SIZE[1])
        pygame.draw.rect(screen, SNAKE_COLOR, segment_rect)

    # draw food
    food_rect = pygame.Rect(game.food.position[1] * GRID_SIZE[0],
                            game.food.position[0] * GRID_SIZE[1],
                            GRID_SIZE[0], GRID_SIZE[1])
    pygame.draw.rect(screen, FOOD_COLOR, food_rect)

    pygame.display.flip()
    clock.tick(20) # limits fps to 60

pygame.quit()