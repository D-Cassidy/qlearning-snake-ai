#! /usr/bin/env python3

# imports
import pygame

# pygame setup
pygame.init()

dark_gray = (38, 38, 38)
window_size = (1280, 1280)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # fill screen with a color to wipe away last frame
    screen.fill(dark_gray)

    # render game here

    # flip() display to put your work on screen
    pygame.display.flip()

    clock.tick(60) # limits fps to 60

pygame.quit()
