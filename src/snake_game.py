class Game:
    def __init__(self, grid_size):
        self.snake = Snake(grid_size)
        self.food = Food(grid_size)
        self.score = 0
        self.game_over = False

    def update(self):
        pass

    def check_collisions(self):
        pass

    def reset(self):
        self.__init__(self.grid_size)

class Snake:
    pass

class Food:
    pass