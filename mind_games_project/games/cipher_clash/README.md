# Cipher Clash

A fast-paced, competitive game where players must decrypt coded messages using different types of classic ciphers (Caesar, Vigenère, Morse, etc.) within a time limit. Points are earned for correct decryptions, and players race against time — or each other — to be the top codebreaker.

## Game Features

- **Multiple Cipher Types**: Caesar, Vigenère, Morse Code, Substitution, and Transposition ciphers
- **Difficulty Levels**: Easy, Medium, and Hard modes with different time limits and scoring
- **Hint System**: Limited hints available to help with difficult puzzles
- **Scoring System**: Points awarded based on accuracy and difficulty
- **Futuristic UI**: Terminal-style interface with neon glowing elements
- **Sound Effects**: Immersive audio feedback for game actions

## How to Play

1. Select a difficulty level and cipher type (or choose Random)
2. Decrypt the encoded message before time runs out
3. Type your answer in the input box and press Enter or click Submit
4. Earn points for correct answers and try to beat your high score

## Cipher Types

- **Caesar Cipher**: A substitution cipher where each letter is shifted by a fixed number of positions
- **Vigenère Cipher**: A method of encrypting text using a series of interwoven Caesar ciphers based on a keyword
- **Morse Code**: A code that uses dots and dashes to represent letters and numbers
- **Substitution Cipher**: A cipher that replaces each letter with another letter or symbol
- **Transposition Cipher**: A cipher that rearranges the positions of characters without changing them

## Game Modes

- **Solo Mode**: Play alone and try to solve as many ciphers as possible within the time limit
- **1v1 Battle**: Compete against another player or the computer to solve ciphers faster

## Requirements

- Python 3.6+
- Pygame 2.0+

## Installation

The game is part of the Mind Games collection. No additional installation is required beyond the main project dependencies.

## Development

### Running Tests

To run the unit tests for the cipher algorithms:

```bash
python -m unittest games.cipher_clash.tests.test_ciphers
```

To run the unit tests for the game logic:

```bash
python -m unittest games.cipher_clash.tests.test_gameplay
```

### Project Structure

- `main.py`: Entry point for the game
- `config.py`: Game configuration settings
- `game_engine/`: Core game logic and cipher algorithms
- `ui/`: User interface components and screens
- `assets/`: Game assets (images, sounds, fonts)
- `data/`: Game data files
- `tests/`: Unit tests

## Credits

- Game concept and development: Mind Games Team
- Cipher algorithms: Based on classical cryptography techniques
- UI design: Inspired by futuristic hacker aesthetics
