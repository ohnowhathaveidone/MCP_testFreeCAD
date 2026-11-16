import os
import json

def load_config():
    """Loads LLM connection settings from the data folder."""
    config_path = "data/config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}. Please create one.")

    with open(config_path, "r") as f:
        return json.load(f)

