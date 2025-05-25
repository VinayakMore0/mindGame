# Mind Meld

A fast-paced memory and reaction game where players memorize and recreate patterns.

## Game Description

Mind Meld challenges your memory and reaction time. The game shows you a pattern for a few seconds, then you must recreate it from memory. Each level gets progressively harder with longer patterns and less time to memorize them.

## Game Modes

- **Single Player Mode**: Challenge yourself to reach the highest level and score.
- **Two Player Mode**: Take turns memorizing and recreating patterns, competing for the highest score.

## How to Play

1. Watch carefully as a pattern appears on the grid.
2. After the pattern disappears, click on the grid cells in the same order to recreate the pattern.
3. Successfully recreate the pattern to advance to the next level.
4. The game ends when you fail to recreate a pattern correctly.

## Controls

- **Mouse**: Click on grid cells to select them.
- That's it! The game is designed to be simple and intuitive.

## Requirements

- Python 3.x
- Pygame

## Installation

1. Make sure you have Python installed
2. Install Pygame: `pip install pygame`
3. Run the game: `python main.py`

## Game Structure

- `main.py`: Entry point for the game
- `game.py`: Core game loop and logic
- `pattern_generator.py`: Creates patterns to be memorized
- `player_input.py`: Handles player input to recreate patterns
- `config.py`: Game settings
- `utils/helpers.py`: Utility functions
- `levels/level_data.json`: Level progression data

## Features

- Progressive difficulty with longer patterns and shorter display times
- Visual feedback for correct and incorrect patterns
- Score system with time bonuses for quick responses
- Two-player competitive mode
- Simple, clean interface

## Sound Credits

The game uses the following sound effects:
- `success.wav`: Sound when pattern is matched correctly
- `fail.wav`: Sound when pattern is matched incorrectly
- `click.wav`: Sound when clicking on grid cells

To add your own sounds, place WAV files in the `assets/sounds/` directory.
