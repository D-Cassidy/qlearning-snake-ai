import random

class Game:
    def __init__(self, grid_size, window_size):
        self.grid_size = grid_size
        self.window_size = window_size
        self.snake = Snake(grid_size)
        self.food = Food(grid_size, window_size)
        self.score = 0
        self.game_over = False

    def update(self):
        self.snake.move()
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.respawn()
            self.score += 1
        self.check_collisions()

    def check_collisions(self):
        head = self.snake.body[0]
        if (head in self.snake.body[1:]
            or head[0] < 0 or head[0] >= (self.window_size[0] / self.grid_size[0])
            or head[1] < 0 or head[1] >= (self.window_size[1] / self.grid_size[1])):
            self.game_over = True

    def reset(self):
        self.__init__(self.grid_size, self.window_size)

class Snake:
    def __init__(self, grid_size):
        self.body = [(5, 5), (5, 4), (5, 3)]
        self.direction = (0, 1)
        self.grid_size = grid_size

    def move(self):
        head = (self.body[0][0] + self.direction[0],
                self.body[0][1] + self.direction[1])
        self.body = [head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])

    def change_direction(self, direction):
        if direction != (-self.direction[0], -self.direction[1]):
            self.direction = direction

class Food:
    def __init__(self, grid_size, window_size):
        self.grid_size = grid_size
        self.window_size = window_size
        self.spawn_food()

    def spawn_food(self):
        self.position = (random.randint(0, int(self.window_size[0] / self.grid_size[0]) - 1),
                random.randint(0, int(self.window_size[1] / self.grid_size[1]) - 1))
    
    def respawn(self):
        self.spawn_food()