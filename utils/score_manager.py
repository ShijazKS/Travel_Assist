import json
import os

# Define the correct path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this script
DATA_DIR = os.path.join(BASE_DIR, "../data")  # Move to /data/ relative to /utils/
FILE_PATH = os.path.join(DATA_DIR, "scores.json")  # Path to scores.json

def save_scores(state, category_scores):

    # Ensure the /data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Load existing data if the file exists
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
    else:
        data = {"global_preferences": {}, "state_preferences": {}}

    # Update global preferences
    for category, values in category_scores.items():
        if category not in data["global_preferences"]:
            data["global_preferences"][category] = {"reward": 0, "count": 0}

        data["global_preferences"][category]["reward"] += values["reward"]
        data["global_preferences"][category]["count"] += values["count"]

    # Update state preferences
    if state not in data["state_preferences"]:
        data["state_preferences"][state] = {}

    for category, values in category_scores.items():
        if category not in data["state_preferences"][state]:
            data["state_preferences"][state][category] = {"reward": 0, "count": 0}

        data["state_preferences"][state][category]["reward"] += values["reward"]
        data["state_preferences"][state][category]["count"] += values["count"]

    # Save the updated data back to the file
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Scores updated and saved to {FILE_PATH}")
