import utils

class SnakeGameWrapper:
    def __init__(self, game):
        self.game = game

    def reset(self):
        """Resets the game and returns the initial state"""
        self.game.reset()
        return self.get_state()
    
    def get_state(self):
        """Retruns the current game state"""
        snake_head = self.game.snake.body[0]
        food_position = self.game.food.position
        x_dist_from_food = snake_head[0] - food_position[0]
        y_dist_from_food = snake_head[1] - food_position[1]
        state = (snake_head, x_dist_from_food, y_dist_from_food)
        return state
    
    def take_action(self, action):
        """Applies chosen action to the game and returns next_state and reward"""
        # Apply action
        if action == 'up':
            self.game.snake.change_direction(utils.UP)
        elif action == 'down':
            self.game.snake.change_direction(utils.DOWN)
        elif action == 'left':
            self.game.snake.change_direction(utils.LEFT)
        elif action == 'right':
            self.game.snake.change_direction(utils.RIGHT)

        old_score = self.game.score
        self.game.update()
        next_state = self.get_state()

        # Define reward
        reward = -1          # default penalty to encourage efficiency
        if self.game.score > old_score:
            reward = 100     # positive reward for food 
        elif self.game.game_over:
            reward = -200    # negative reward for losing

        done = self.game.game_over
        return next_state, reward, done