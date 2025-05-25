"""
Shared utility functions for the Mind Games project.
Contains helper functions used across all games.
"""

import os
import json
import time
import random
from functools import wraps

def timed_function(func):
    """
    Decorator to measure the execution time of a function.
    
    Args:
        func: The function to time
        
    Returns:
        The wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds to run")
        return result
    return wrapper

def load_json_file(file_path):
    """
    Load data from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict: The loaded JSON data or an empty dict if the file doesn't exist
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not a valid JSON file")
        return {}
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}

def save_json_file(file_path, data):
    """
    Save data to a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        data (dict): Data to save
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

def clamp(value, min_value, max_value):
    """
    Clamp a value between a minimum and maximum.
    
    Args:
        value: The value to clamp
        min_value: The minimum allowed value
        max_value: The maximum allowed value
        
    Returns:
        The clamped value
    """
    return max(min_value, min(value, max_value))

def weighted_choice(choices):
    """
    Make a weighted random choice from a list of options.
    
    Args:
        choices (list): List of (option, weight) tuples
        
    Returns:
        The selected option
    """
    total = sum(weight for _, weight in choices)
    r = random.uniform(0, total)
    upto = 0
    for choice, weight in choices:
        if upto + weight >= r:
            return choice
        upto += weight
    # Fallback to last item (should not happen)
    return choices[-1][0]

def format_time(seconds):
    """
    Format seconds into a time string (MM:SS).
    
    Args:
        seconds (int): Number of seconds
        
    Returns:
        str: Formatted time string
    """
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"

def calculate_score(base_points, time_taken, difficulty_multiplier, accuracy=1.0):
    """
    Calculate a score based on points, time, difficulty, and accuracy.
    
    Args:
        base_points (int): Base points earned
        time_taken (float): Time taken in seconds
        difficulty_multiplier (float): Multiplier based on difficulty
        accuracy (float): Accuracy as a decimal (0.0 to 1.0)
        
    Returns:
        int: The calculated score
    """
    time_factor = max(0.1, 1.0 - (time_taken / 300))  # Time bonus decreases as time increases
    return int(base_points * difficulty_multiplier * time_factor * accuracy)

def get_high_scores(game_id, max_entries=10):
    """
    Get high scores for a specific game.
    
    Args:
        game_id (str): ID of the game
        max_entries (int): Maximum number of high scores to return
        
    Returns:
        list: List of high score entries
    """
    scores_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              "data", "high_scores.json")
    scores_data = load_json_file(scores_file)
    
    # Get scores for the specific game
    game_scores = scores_data.get(game_id, [])
    
    # Sort by score (descending) and limit to max_entries
    return sorted(game_scores, key=lambda x: x.get('score', 0), reverse=True)[:max_entries]

def save_high_score(game_id, player_name, score, difficulty):
    """
    Save a high score for a specific game.
    
    Args:
        game_id (str): ID of the game
        player_name (str): Name of the player
        score (int): Score achieved
        difficulty (str): Difficulty level
        
    Returns:
        bool: True if successful, False otherwise
    """
    scores_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              "data", "high_scores.json")
    scores_data = load_json_file(scores_file)
    
    # Initialize game scores if not present
    if game_id not in scores_data:
        scores_data[game_id] = []
    
    # Add new score
    scores_data[game_id].append({
        'player': player_name,
        'score': score,
        'difficulty': difficulty,
        'date': time.strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Sort scores and keep only top 100
    scores_data[game_id] = sorted(
        scores_data[game_id], 
        key=lambda x: x.get('score', 0), 
        reverse=True
    )[:100]
    
    # Save updated scores
    return save_json_file(scores_file, scores_data)
