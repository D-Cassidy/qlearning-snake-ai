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
        snake_body = self.game.snake.body[1:]
        food_position = self.game.food.position
        state = tuple([snake_head] + snake_body + [food_position])
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

        self.game.update()
        next_state = self.get_state()

        # Define reward
        reward = 0
        if self.game.snake.body[0] == self.game.food.position:
            reward = 150     # positive reward for food 
        elif self.game.game_over:
            reward = -250    # negative reward for losing
        else:
            reward = -1     # light punishment for getting nothing done

        done = self.game.game_over
        return next_state, reward, done