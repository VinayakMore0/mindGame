# Logic Arena

A turn-based logic puzzle game where players solve mini brain teasers and visual logic questions within a time limit.

## Game Description

Logic Arena challenges your logical thinking and pattern recognition skills. The game presents you with various types of logic puzzles, including:

- Sequence completion
- Number pattern recognition
- Odd-one-out identification
- Grid-based deduction puzzles

Each correct answer increases your score, and the difficulty increases as you progress.

## Game Modes

- **Solo Mode**: Challenge yourself to solve as many puzzles as possible and achieve the highest score.
- **Versus Mode**: Compete against another player in a turn-based format, with each player taking turns to solve puzzles.

## How to Play

1. Select a game mode (Solo or Versus).
2. A logic puzzle will appear on the screen.
3. Choose the correct answer from the options provided.
4. Answer within the time limit to earn points.
5. The faster you answer, the more bonus points you earn.
6. In Solo mode, wrong answers reduce your remaining time.
7. In Versus mode, players take turns answering questions.

## Controls

- **Mouse**: Click on the option buttons to select your answer.
- **Keyboard**: Press 1-4 to select the corresponding option.

## Requirements

- Python 3.x
- Pygame

## Installation

1. Make sure you have Python installed
2. Install Pygame: `pip install pygame`
3. Run the game: `python main.py`

## Game Structure

- `main.py`: Entry point for the game
- `game.py`: Main game loop and scene controller
- `question_manager.py`: Handles logic question generation and validation
- `player_input.py`: Captures and verifies answers from user
- `config.py`: Game settings
- `questions/`: JSON files containing logic puzzles by difficulty
- `utils/helpers.py`: Utility functions

## Features

- Progressive difficulty system
- Time-based scoring with bonuses for quick answers
- Visual feedback for correct and incorrect answers
- Two-player competitive mode
- Various types of logic puzzles

## Adding Custom Questions

You can add your own questions by editing the JSON files in the `questions/` directory. Each question should follow this format:

```json
{
  "type": "sequence",
  "question": "What comes next in this sequence?",
  "sequence": [1, 2, 3, 4, 5],
  "options": [6, 7, 8, 9],
  "answer": 6
}
```

## Sound Credits

The game uses the following sound effects:
- `correct.wav`: Sound when answer is correct
- `wrong.wav`: Sound when answer is wrong
- `tick.wav`: Countdown tick when time is running low

To add your own sounds, place WAV files in the `assets/sounds/` directory.
