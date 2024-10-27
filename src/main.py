#! /usr/bin/env python3

# imports
import argparse
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
NUM_GRIDS = 20
GRID_SIZE = (int(SIZE/NUM_GRIDS), int(SIZE/NUM_GRIDS))
FONT_SIZE = int(GRID_SIZE[0])

# create pygame screen
WINDOW_SIZE = (SIZE, SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

def main(agent='player', visualization=True):
    # initialize game
    game_speed = 20
    game = Game(GRID_SIZE, WINDOW_SIZE)
    print(f"""Initializing Game:
        Window Size: {WINDOW_SIZE}px
        Grid Size: {GRID_SIZE}px
        Grids: {int(WINDOW_SIZE[0]/GRID_SIZE[0])} x {int(WINDOW_SIZE[1]/GRID_SIZE[1])}
    """)

    # GAME LOOP FOR HUMAN INPUT
    if agent == 'player':
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return
                    elif event.key == pygame.K_UP:
                        game.snake.change_direction(utils.UP)
                    elif event.key == pygame.K_DOWN:
                        game.snake.change_direction(utils.DOWN)
                    elif event.key == pygame.K_LEFT:
                        game.snake.change_direction(utils.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        game.snake.change_direction(utils.RIGHT)
            game.update()
            if game.game_over: game.reset()
            render_game(game, game_speed)

    # GAME LOOP FOR Q-LEARNING AGENT
    elif agent =='q-learn':
        # initialize agent
        actions = ['up', 'down', 'left', 'right']
        wrapper = SnakeGameWrapper(game)
        agent = QLearningAgent(actions)
        agent.load_q_table()

        # training settings
        num_epochs = 100000
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
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            return
                        elif event.key == pygame.K_EQUALS:
                            game_speed += 10
                            print(f"Speed increased to {game_speed}")
                        elif event.key == pygame.K_MINUS:
                            game_speed -=10
                            print(f"Speed decreased to {game_speed}")

                if visualization == True:
                    render_game(game, game_speed)

            # Log progress
            print(f"Epoch {epoch+1}/{num_epochs}, Score: {game.score}, Total Reward: {total_reward}, Epsilon {agent.epsilon:.4f}")
            agent.decay_epsilon()

        agent.save_q_table()

def render_game(game, game_speed):
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
    clock.tick(game_speed) # limits fps to 60

# MAIN SCRIPT
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--agent", type=str, default='player', help='Which AI agent or input mode to use')
    parser.add_argument("--visualization", action='store_false', help='Whether to visualize the game board or not')
    args = parser.parse_args()
    print(args)

    main(agent=args.agent, visualization=args.visualization)
    pygame.quit()