# Mind Games Project

A collection of brain-teasing puzzle games designed to challenge your mental abilities.

## Games Included

### Cipher Clash
Test your cryptography skills by decrypting various types of ciphers against the clock.

### Quantum Maze
Navigate through a maze where the paths change based on quantum probability principles.

### Mind Meld
A pattern recognition game where you must synchronize your thinking with the computer.

### Logic Arena
Solve complex logic puzzles and compete against an AI opponent.

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/mind_games_project.git
cd mind_games_project
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

Run the launcher to start the application:
```
python launcher.py
```

Select a game from the menu to begin playing.

## Project Structure

```
mind_games_project/
├── launcher.py                # Main entry point
├── games/                     # Individual games
│   ├── cipher_clash/          # Cryptography puzzle game
│   ├── quantum_maze/          # Quantum-based maze game
│   ├── mind_meld/             # Pattern recognition game
│   └── logic_arena/           # Logic puzzle game
├── shared/                    # Shared utilities and settings
├── assets/                    # Shared assets
└── requirements.txt           # Python dependencies
```

## Game Descriptions

### Cipher Clash
Decrypt messages encoded with various cipher techniques, including Caesar, Atbash, Vigenère, and more. Race against the clock to solve as many as possible.

### Quantum Maze
Navigate through a maze where paths change based on quantum probability. The maze reconfigures itself as you move through it, creating a unique challenge each time.

### Mind Meld
Identify patterns and synchronize your thinking with the computer. The game analyzes your responses and adapts to your thought patterns.

### Logic Arena
Solve complex logic puzzles of increasing difficulty. Compete against an AI opponent that learns from your strategies.

## Development

Each game is modular and can be developed independently. To add a new game:

1. Create a new directory under `games/`
2. Implement the required modules and assets
3. Update the launcher to include your new game

## License

This project is licensed under the MIT License - see the LICENSE file for details.
