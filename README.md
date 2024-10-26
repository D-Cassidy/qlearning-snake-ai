# Snake AI Game

A self-learning AI that plays the classic Snake game, developed in Python. This project includes a basic 
PyGame based version of Snake and reinforcement learning (Q-learning) to train an AI to improve its gameplay performance.

### Table of Contents
- [Project Overview](#project-overview)
- [Q-Learning Agent](#q-learning-agent)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)

### Project Overview
The goal of this project is to teach myself more about how AI, in particular reinforcement learning works with 
the added benefit of learning the PyGame library. It features a Snake Game made using Python's PyGame library 
and a Q-Learning agent trying to improve at the game using the epsilon-greedy algorithm.

### Q-Learning Agent
#### Iteration 1:
The state is represented only by the location of the snake's head and the position of the food.
epsilon_decay = 0.995, min_epsilon = 0.01
Rewards: +10 for finding food, -10 for losing, and -1 for nothing happening.

The snake seems to have learned to off itself as soon as possible since the game board is so large it 
cannot possibly find enough food fast enough to outdo the -1 reward for each move. Need to tweak the reward values.

#### Iteration 2:
The state is still only represented by the location of the snake's head and the position of the food. 
I forsee this becoming a problem as the snake gets longer, as it doesn't know where the body is 
epsilon_decay = 0.999, min_epsilon = 0.01
Rewards: +150 for finding food, -250 for losing, and -1 for nothing happening.

### Installation
1. Clone repository:
    ```bash
    git clone https://github.com/D-Cassidy/snake-ai-game.git
    cd snake-ai-game
    ```

2. Setup virtual environment (optional):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install packages:
    ```bash
    pip install -r requirements.txt
    ```

### Usage
1. Run the game:
    ```bash
    ./src/main.py
    ```

2. Training the AI:
    TODO

### Project Structure
```plaintext
snake-ai-game/
|
|--src/
|   |--main.py                  # Main game loop
|   |--snake_game.py            # Game logic for snake and food
|   |--qlearning_ai_agent.py    # AI agent
|   |--game_wrapper.py          # wrapper for interfacing between game and AI agent
|   |--utils.py                 # Helper functions
|
|--models/
|   |--q_table.pkl              # saves data on ai agent
|
|--requirements.txt             # Project dependencies
|--README.md                    # Project documentation
|--LICENSE                      # MIT License
```
