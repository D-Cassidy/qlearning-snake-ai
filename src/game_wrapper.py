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
        y_dist_from_food = snake_head[0] - food_position[0]
        x_dist_from_food = snake_head[1] - food_position[1]
        # Get food direction to reduce size of state space
        x_dir_to_food = -1 if x_dist_from_food < 0 else 1
        y_dir_to_food = -1 if y_dist_from_food < 0 else 1

        vision = []
        for i in range(-1, 2, 2):
            square1 = (snake_head[0]+i, snake_head[1])
            square2 = (snake_head[0], snake_head[1]+i)
            vision.append(square1 in self.game.snake.body 
                          or square1[0] < 0 or square1[0] > (self.game.window_size[0] / self.game.grid_size[0])
                          or square1[1] < 0 or square1[1] > (self.game.window_size[1] / self.game.grid_size[1]))
            vision.append(square2 in self.game.snake.body 
                          or square2[0] < 0 or square2[0] > (self.game.window_size[0] / self.game.grid_size[0])
                          or square2[1] < 0 or square2[1] > (self.game.window_size[1] / self.game.grid_size[1]))

        vision = tuple(vision)

        state = (-x_dir_to_food, y_dir_to_food, vision)
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
        reward = -2          # default penalty to encourage efficiency
        if self.game.score > old_score:
            reward = 500     # positive reward for food 
        elif self.game.game_over:
            reward = -100    # negative reward for losing

        done = self.game.game_over
        return next_state, reward, done