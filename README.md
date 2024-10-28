# Q-Learning Snake AI

A self-learning AI that plays the classic Snake game, developed in Python. This project includes a basic 
PyGame based version of Snake and reinforcement learning (Q-learning) to train an AI to improve its gameplay performance.

### Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Q-Learning Agent](#q-learning-agent)
- [Project Structure](#project-structure)


### Project Overview
The goal of this project is to teach myself more about how AI, in particular reinforcement learning works with 
the added benefit of learning the PyGame library. It features a Snake Game made using Python's PyGame library 
and a Q-Learning agent trying to improve at the game using the epsilon-greedy algorithm.


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
1. Run the game with default settings
    ```bash
    src/main.py 
    ```

2. Run the game with AI player
    ```bash
    src/main.py --agent 'q-learn' --file 'models/iter5_q_table.pkl'
    ```

**Parameters** 
- --agent | type=str | options='player', 'q-learn' | which agent will be used to play the game 
- --visualization | True by default, using this flag will toggle to False
- --epochs | type=int | Number of epochs the AI will train for if using AI agent
- --file | type=str | Which file to load AI agent from, be sure to use relative path from main directory

### Q-Learning Agent

This section documents the tweaks and AI performance over time for the Q-learning agent.

### Initial Setup
- **Parameters**:
  - **Learning Rate (α)**: `0.1`
  - **Discount Factor (γ)**: `0.9`
  - **Epsilon (ε)**: `1.0`, with **Decay**: `0.995`
  - **Rewards**:
    - Food: `10`
    - Step Penalty: `-1`
    - Wall Collision: `-10`
- **State Representation**: Absolute head position, absolute food position.
- **Observations**: After learning for a few iterations, it seems to have learned to off itself as soon as possible to minimize negative rewards.

#### Iteration 1:
- **Changes**
    - **Increased Food Reward** to +50
    - **Increased Losing Penalty** to -100
    - **Removed default penalty**
    - **Added reward** for moving towards the food (+2)
    - **Added penalty** for moving away from food (-1)
- **Observations**: this iteration was allowed to train for much longer than the last one. It seems to have learned go in circles rather than die to 'farm' infinite reward. Just repeating +2 for going towards food, -1 for going away from food. Whoops. It also takes immensely long to train but the score got as high as 30, previous iteration only ever got to 4.

#### Iteration 2:
- **Changes**
    - **Increased Food Reward** to +100
    - **Increased Losing Penalty** to -200
    - **Added default penalty** of -1 for nothing happening
    - **Removed reward/penalty** for moving towards/away from food
    - **Changed state given** to include relative position of snake to food, rather than absolute position of food
- **Observations**: This one seems to learn very slowly which I didn't expect. I added the ability to turn off the game visualization so it can train much faster but it seems to be worse than the last iteration despite twice the training. I guess the reward for moving towards the food was quite important, but I think I'll just tweak the parameters and try again.

#### Iteration 3:
- **Changes**
    - **Epsilon Decay** to 0.999
    - **Minimum Epsilon** to 0.1
    - **Increased Food Reward** to +500
    - **Decreased Losing Penalty** to -100
    - **Increased step penalty** to -2
- **Observations**: I've realized that the state-action space is simply too large for this to converge to a consistent behavior. I'm gonig to reset the parameters to the initial setup and make the state given simply the relative position to food and nothing else.

#### Iteration 4: 
- **Changes**
    - **Epsilon Decay** to 0.995
    - **Minimum Epsilon** to 0.01
    - **Changed State Tuple** to include only relative position to food to reduce state-action space size
- **Observations**: After training for just 10000 iterations the behavior is clear, it has learned to move towards the food. Decreasing the size of the state-action space was the right move and now it's dying more often to its own body than walls.

#### Iteration 5:
- **Changes**
    - **Change state tuple** to just give direction to food instead of distance
    - **Change state tuple** to include what is currently in each grid adjacent to the snake
- **Observations**: By far the most successful version. This iteration displays clear behavior of having 'learned' the game and only struggles with the game when the snake gets too long and it boxes itself in. This is probably the limit of Q-Learning as I can't think of any ways to improve it aside from giving it more information which would increase the size of the state-action space too much for vanilla Q-Learning.

#### Summary
After achieving a successful AI on iteration 5 that appears to display intelligent behavior in its gameplay the Q-Learning project is completed. In early iterations the state-action space was simply too large (upwards of 2000000 possible state-action combinations by my calculations) to train in a reasonable amount of time. The solution was come up with a method of giving it information that would be useful and create as few unique state-action combinations as possible. In the end I settled giving the x direction of the food (-1, 1, or 0), the y direction of the food (-1, 1, or 0), and whether or not there was a collidable object on any of the spaces immediately adjacent to the head (True or False). The penalty for taking any step at all also seems to have had the intended effect of getting the AI to favor shorter paths.

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
|   |--*.pkl              # saves data on ai agent
|
|--requirements.txt             # Project dependencies
|--README.md                    # Project documentation
|--LICENSE                      # MIT License
```
