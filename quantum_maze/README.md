# Quantum Maze

A simple maze game with quantum mechanics-inspired gameplay elements.

## Game Description

In Quantum Maze, you navigate through a series of mazes using both traditional movement and quantum abilities:

- **Traditional Movement**: Use arrow keys or WASD to move through the maze
- **Quantum Position Storage**: Press Q to store your current position in quantum memory
- **Quantum Teleportation**: Press E to teleport to a previously stored position

Your goal is to reach the exit (green square) in each level while managing your quantum energy.

## Controls

- **Movement**: Arrow keys or WASD
- **Store Position**: Q key
- **Quantum Teleport**: E key

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
- `maze.py`: Maze layout and rendering
- `player.py`: Player movement and quantum abilities
- `config.py`: Game settings
- `levels/`: Text files defining maze layouts
- `assets/`: Game assets (images, sounds, fonts)

## How to Create Custom Levels

Create a text file in the `levels/` directory with the following format:
- `#`: Wall
- `.`: Floor
- `P`: Player starting position
- `E`: Exit

Example:
```
#####
#P..#
#.#.#
#..E#
#####
```
