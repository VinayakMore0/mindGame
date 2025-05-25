````markdown
# 🧠 Mind Games Collection — Built with Pygame

Welcome to **Mind Games**, a collection of four fun, competitive, and brain-boosting mini-games built using Python and Pygame. Each game is simple to play, easy to build, and designed to test a different mental skill — from memory to logic, speed, and reasoning.

---

## 🎮 Included Games

| Game Name      | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| 🔐 Cipher Clash | Crack scrambled codes and decipher hidden words under time pressure        |
| 🌀 Quantum Maze | Navigate a shifting digital maze — test your reaction and timing            |
| 🧠 Mind Meld     | Memory-based challenge: remember and repeat patterns before time runs out  |
| 🧩 Logic Arena   | Solve turn-based visual and numerical logic puzzles to score points        |

---

## 🚀 Getting Started

### ✅ Requirements

- Python 3.8 or later
- `pygame` library

Install Pygame using pip:

```bash
pip install pygame
````

---

### 🗂️ Project Structure

```
mind_games/
├── game_launcher/           # Main launcher UI to pick a game
│   ├── main.py
│   └── launcher_ui.py
├── cipher_clash/
├── quantum_maze/
├── mind_meld/
├── logic_arena/
└── README.md
```

Each game is self-contained inside its own folder. You can run any game directly or launch them through the main game launcher.

---

## 🧩 Game Instructions

### 🔐 Cipher Clash

* **Type**: Word Puzzle / Code Breaking
* **Goal**: Decode ciphers (e.g., Caesar shift, jumbled letters) before the timer runs out.
* **Modes**: Single Player, 2-Player Turn-Based
* **How to Play**: Unscramble the code and submit your guess.

### 🌀 Quantum Maze

* **Type**: Reflex & Navigation
* **Goal**: Escape the shifting digital maze without hitting traps.
* **Mechanics**: Use arrow keys to move, but beware — walls might teleport or disappear!

### 🧠 Mind Meld

* **Type**: Memory
* **Goal**: Memorize and repeat color/shape/position patterns.
* **Rounds**: Gets harder as you go. Limited time for recall.
* **Multiplayer Mode**: Take turns and compete for score.

### 🧩 Logic Arena

* **Type**: Logic & Reasoning
* **Goal**: Solve visual or numerical puzzles quickly and accurately.
* **Puzzle Types**: Pattern recognition, odd-one-out, sequences.
* **Scoring**: Based on speed and correctness.

---

## 🧑‍💻 Developer Guide

* Each game folder contains:

  * `main.py` – Entry point
  * `game.py` – Core loop and rendering
  * `assets/` – Images, sounds, fonts
  * `config.py` – Settings like resolution, timer
  * `utils/` – Helper functions
* To **launch a game**:

  ```bash
  python mind_games/cipher_clash/main.py
  ```

  Or use the launcher:

  ```bash
  python mind_games/game_launcher/main.py
  ```

---

## 📦 Assets & Acknowledgments

All assets (images, fonts, sounds) are free-to-use and open-source. Sources include:

* [Kenney.nl](https://kenney.nl/) – Game assets
* [Google Fonts](https://fonts.google.com/) – Fonts
* [Freesound.org](https://freesound.org/) – Sound effects

---

## 🧠 Built With

* [Python 3](https://www.python.org/)
* [Pygame](https://www.pygame.org/)

---

## 📌 Roadmap

* [ ] Add high score tracking
* [ ] Online multiplayer for Cipher Clash
* [ ] Difficulty selection for all games
* [ ] Save/load progress

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙌 Contributions Welcome!

Feel free to fork the repo, suggest changes, or create new mini-games that fit into the launcher. Contributions are appreciated!

---

Made with ❤️ and Python by \[Your Name].

```

---

