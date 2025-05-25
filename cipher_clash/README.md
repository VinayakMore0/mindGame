# Cipher Clash

A fast-paced code-breaking game where players decode scrambled letters, numbers, or patterns to find hidden words or sequences.

## Game Description

Cipher Clash challenges your code-breaking skills with various types of ciphers:

- **Caesar Cipher**: Letters shifted by a specific amount
- **Substitution Cipher**: Letters replaced with other letters
- **Jumbled Words**: Letters rearranged
- **Morse Code**: Dots and dashes representing letters
- **Binary Code**: Binary or hexadecimal representations

Decode the ciphers as quickly as possible to earn points and advance to more difficult challenges.

## Game Modes

- **Single Player Mode**: Decode as many ciphers as possible before time runs out.
- **Two Player Mode**: Turn-based cipher solving — score points based on speed and accuracy.

## How to Play

1. Select a game mode (Single Player or Two Player).
2. A cipher will appear on the screen.
3. Type your answer in the input box and press Enter.
4. You have a limited number of attempts for each cipher.
5. Solve ciphers quickly to earn time bonuses and build a streak for additional points.
6. Click the "Hint" button if you need help.

## Controls

- **Mouse**: Click on the input box to activate it, and click the Hint button for hints.
- **Keyboard**: Type your answer and press Enter to submit.

## Requirements

- Python 3.x
- Pygame

## Installation

1. Make sure you have Python installed
2. Install Pygame: `pip install pygame`
3. Run the game: `python main.py`

## Game Structure

- `main.py`: Game entry point
- `game.py`: Game loop and state manager
- `cipher_engine.py`: Handles cipher generation and checking
- `player_input.py`: Collects and verifies input from player
- `config.py`: Game settings
- `ciphers/`: Word bank and sample ciphers
- `utils/helpers.py`: Utility functions

## Features

- Multiple cipher types with varying difficulty
- Progressive difficulty system
- Time-based scoring with streak bonuses
- Hint system for challenging ciphers
- Two-player competitive mode
- Retro hacker aesthetic with matrix-style visuals

## Adding Custom Words

You can add your own words to the word bank by editing the `ciphers/word_bank.txt` file. Each word should be on a new line.

## Sound Credits

The game uses the following sound effects:
- `correct.wav`: Sound when answer is correct
- `wrong.wav`: Sound when answer is wrong
- `tick.wav`: Countdown tick when time is running low

To add your own sounds, place WAV files in the `assets/sounds/` directory.
