#! /usr/bin/env python3

# imports
import pygame

from snake_game import Game
from game_wrapper import SnakeGameWrapper
from qlearning_ai_agent import QLearningAgent
import utils

# pygame setup
pygame.init()

# colors
BACKGROUND_COLOR = (38, 38, 38)
SNAKE_COLOR = (0, 168, 37)
FOOD_COLOR = (222, 0, 0)
SCORE_COLOR = (255, 255, 255)

# constants
MONITOR_DIM = (pygame.display.Info().current_w, pygame.display.Info().current_h)
SIZE = int(min(MONITOR_DIM) * 0.9)
GRID_SIZE = (int(SIZE/40), int(SIZE/40))
FONT_SIZE = int(GRID_SIZE[0]*2)

# create pygame screen
WINDOW_SIZE = (SIZE, SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

# initialize game
game = Game(GRID_SIZE, WINDOW_SIZE)
print(f"""Initializing Game:
    Window Size: {WINDOW_SIZE}px
    Grid Size: {GRID_SIZE}px
    Grids: {int(WINDOW_SIZE[0]/GRID_SIZE[0])} x {int(WINDOW_SIZE[1]/GRID_SIZE[1])}
""")

# initialize agent
actions = ['up', 'down', 'left', 'right']
wrapper = SnakeGameWrapper(game)
agent = QLearningAgent(actions)

# training settings
num_epochs = 1000
for epoch in range(num_epochs):
    state = wrapper.reset()
    done = False 
    total_reward = 0    # track reward per epoch

    while not done:
        # ai agent
        action = agent.choose_action(state)
        next_state, reward, done = wrapper.take_action(action)
        agent.update_q_table(state, action, reward, next_state)
        state = next_state
        total_reward += reward

        # poll for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
        

        # fill screen with a color to wipe away last frame
        screen.fill(BACKGROUND_COLOR)

        # RENDER GAME
        # draw snake
        for segment in game.snake.body:
            seg_x = segment[1] * GRID_SIZE[0]
            seg_y = segment[0] * GRID_SIZE[1]
            segment_rect = pygame.Rect(seg_x, seg_y, GRID_SIZE[0], GRID_SIZE[1])
            pygame.draw.rect(screen, SNAKE_COLOR, segment_rect)

        # draw food
        food_radius = GRID_SIZE[0]/2
        food_x = game.food.position[1] * GRID_SIZE[0] + food_radius
        food_y = game.food.position[0] * GRID_SIZE[1] + food_radius
        pygame.draw.circle(screen, FOOD_COLOR, (food_x, food_y), food_radius)

        # display score
        score_font = pygame.font.Font(size=FONT_SIZE)
        score_text = score_font.render(f"Score: {game.score}", True, SCORE_COLOR)
        screen.blit(score_text, (int(SIZE/2) - int(score_text.get_size()[0]/2), 10))

        # display high score
        try: high_score = max(high_score, game.score)
        except NameError: high_score = 0
        high_score_font = pygame.font.Font(size=int(FONT_SIZE/2))
        high_score_text = high_score_font.render(f"High Score: {high_score}", True, SCORE_COLOR)
        screen.blit(high_score_text, (10, 10))


        pygame.display.flip()
        clock.tick(20) # limits fps to 60

    # Log progress
    print(f"Epoch {epoch+1}/{num_epochs}, Score: {game.score}, Total Reward: {total_reward}, Epsilon {agent.epsilon:.4f}")
    agent.decay_epsilon()

pygame.quit()