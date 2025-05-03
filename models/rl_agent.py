import json
import os
import math

class RLAgent:
    def __init__(self, score_file="data/scores.json"):
        self.categories = ["tourism", "entertainment", "leisure", "natural", "camping", "beach"]
        self.exploration_factor = 2.0  # "c" in UCB formula
        self.scores = self.load_scores(score_file)
        self.total_selections = self.compute_total_selections()
        self.score_file = score_file
        
    # def get_exploration_factor(self):
    #     initial = 2.0
    #     min_val = 0.5
    #     decay_rate = 0.01
    #     return max(min_val, initial * math.exp(-decay_rate * self.total_selections))


    def load_scores(self, file_path):
        """Load global and state-based scores from JSON."""
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return json.load(file)
        return {"global_preferences": {}, "state_preferences": {}}

    def compute_total_selections(self):
        """Compute total selections dynamically to avoid it always being 1."""
        total = sum(reward["count"] for reward in self.scores["global_preferences"].values())
        return total if total > 0 else 1  # Avoid division by zero

    def get_ucb_score(self, rewards, category, total):
        """Calculate UCB score correctly, but don't prioritize count=0 categories."""
        if category not in rewards or rewards[category]["count"] == 0:
            return -float("inf")  # Assign lowest priority instead of high random score

        avg_reward = rewards[category]["reward"] / rewards[category]["count"]
        exploration = self.exploration_factor * math.sqrt(math.log(total + 1) / rewards[category]["count"])
        # exploration = self.get_exploration_factor() * math.sqrt(math.log(total + 1) / rewards[category]["count"])
        return avg_reward + exploration

    def recommend_categories(self, state):
        """Select categories using UCB, combining state and global preferences in a weighted manner."""
        global_rewards = self.scores["global_preferences"]
        state_rewards = self.scores["state_preferences"].get(state, {})

        ucb_scores = []
        for category in self.categories:
            global_ucb = self.get_ucb_score(global_rewards, category, self.total_selections)
            state_ucb = self.get_ucb_score(state_rewards, category, self.total_selections)

            # Dynamically assign weight based on whether state has past data
            state_weight = len(state_rewards) / (len(state_rewards) + len(global_rewards)) if state_rewards else 0.0

            # If state data is missing, fall back to global UCB
            final_ucb = (1 - state_weight) * (global_ucb if global_ucb != -float("inf") else 0) + state_weight * (state_ucb if state_ucb != -float("inf") else 0)

            ucb_scores.append((category, final_ucb))
        print(ucb_scores)
        # Sort categories based on UCB score (highest first)
        sorted_categories = [cat for cat, _ in sorted(ucb_scores, key=lambda x: x[1], reverse=True)]
        return sorted_categories
