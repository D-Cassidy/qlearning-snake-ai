import os 
import random
import pickle

class QLearningAgent:
    def __init__(self, actions, 
                 alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.01, 
                 q_table_file='models/q_table.pkl'):
        self.actions = actions 
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon 
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.q_table = {}
        self.q_table_file = q_table_file

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0)
    
    def choose_action(self, state):
        # epsilon-greedy action selection
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions) # explore
        else:
            # exploit
            q_values = {action: self.get_q_value(state, action) for action in self.actions}
            return max(q_values, key=q_values.get)
        
    def update_q_table(self, state, action, reward, next_state):
        max_next_q = max(self.get_q_value(next_state, a) for a in self.actions)
        current_q = self.get_q_value(state, action)

        # q-learning update rule
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[(state, action)] = new_q

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def save_q_table(self):
        """Save Q-table to a file."""
        with open(self.q_table_file, "wb") as f:
            pickle.dump({'q_table': self.q_table, 'epsilon': self.epsilon}, f)
        print("Q-table and epsilon saved successfully.")

    def load_q_table(self):
        """Load the Q-table from file."""
        try:
            with open(self.q_table_file, "rb") as f:
                data = pickle.load(f)
                self.q_table = data.get('q_table', {})
                self.epsilon = data.get('epsilon', 1.0)     # default to 1.0 if not found
            print("Q-table loaded successfully.")
        except FileNotFoundError:
            print("No Q-table file found. Starting with empty Q-table.")