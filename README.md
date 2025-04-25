# Pac-Man AI Game

A simple text-based Pac-Man game implemented in Python using NumPy. This project demonstrates basic game AI concepts, featuring a Pac-Man agent controlled by the Minimax algorithm (with Alpha-Beta Pruning) and Ghost agents using A* search to chase Pac-Man.

## Features

* **Text-Based Interface:** Renders the game state directly in the terminal.
* **AI-Controlled Pac-Man:** Uses the Minimax algorithm with Alpha-Beta pruning to determine the optimal move based on a heuristic evaluation function.
* **AI-Controlled Ghosts:** Employ A* search algorithm to find the shortest path to Pac-Man's current location.
* **Customizable Layout:** Game board layout is loaded from an external text file (`layout.txt`).
* **Configurable Parameters:** Easily adjust the number of ghosts and the search depth for Pac-Man's AI.
* **Scoring System:** Includes scores for eating dots, penalties for moving, and significant scores for winning or losing.
* **Game State Evaluation:** A heuristic function evaluates game states considering score, distance to ghosts, and remaining dots.

## Requirements

* Python 3.x
* NumPy library


1.  **Install NumPy:**
    ```bash
    pip install numpy
    ```

## Usage

1.  **Prepare the Layout File:**
    * The game requires a `layout.txt` file in the same directory as the script.
    * The script includes a default layout and will **automatically create** `layout.txt` with this content if it doesn't exist.
    * **Layout Characters:**
        * `o`: Wall
        * `.`: Dot (Food)
        * ` `: Empty Space
        * `P`: Pac-Man starting position (only one allowed)
        * `G`: Ghost starting position (optional, ghosts can also start on empty spaces)
        * `*`: Power Pellet (Note: Power pellet logic is *not* currently implemented in the provided code, but the constant exists).
    * **Example `layout.txt`:**
        ```txt
      oooooooooooooooooooo
      oP.................o
      o.ooooooooo.oooooo.o
      o.o.......o..o.....o
      o.o.ooooo.o.o.oooo.o
      o......G...o..o.o..o
      ooooo.o.ooo.oooo.o.o
      oG....o............o
      oooooo.oooooo.oooo.o
      o..................o
      oooooooooooooooooooo
        ```
    * **Important:** The layout *must* be rectangular (all rows must have the same length).

2.  **Run the Game:**
    Execute the Python script from your terminal:
    ```bash
    python pacman_game.py
    ```
    *(Replace `pacman_game.py` with the actual name you saved the script as).*

3.  **Gameplay:**
    The game will run automatically. Pac-Man and the Ghosts will move based on their respective AI algorithms. The game ends when Pac-Man eats all the dots (Win) or gets caught by a ghost (Lose).

## Configuration

You can configure the game by modifying the `if __name__ == "__main__":` block at the end of the script (`pacman_game.py`):

```python
if __name__ == "__main__":
    # --- snip ---

    try:
        # Change number of ghosts and Pac-Man AI depth here
        game = PacmanGame(layout_filename, num_ghosts=2, pacman_ai_depth=4)
        game.run()

    # --- snip ---
```

* `num_ghosts`: Set the desired number of ghosts. If the layout doesn't contain enough `G` characters, ghosts will be placed on available empty spaces (` `).
* `pacman_ai_depth`: Controls how many moves ahead the Pac-Man AI looks (using Minimax). Higher values lead to potentially better decisions but significantly increase computation time per move.

## Code Overview

* **`pacman_game.py` (Main Script):** Contains all the classes and functions.
    * **`Board` Class:** Represents the game grid, handles layout loading, character access, valid moves, and drawing. Uses NumPy array for the layout.
    * **`Pacman` Class:** Represents the Pac-Man agent, manages its position and score.
    * **`Ghost` Class:** Represents a Ghost agent, manages its position and the character it's currently hiding.
    * **`PacmanGame` Class:** Orchestrates the game flow, initializes agents, runs the game loop, and handles game state updates.
    * **AI Functions:**
        * `heuristic()`: Manhattan distance heuristic used by A*.
        * `a_star_search()`: Implements A* pathfinding for ghosts.
        * `evaluate_state()`: Heuristic function to evaluate the "goodness" of a game state for Pac-Man.
        * `simulate_move()`: Creates a hypothetical future game state after a move.
        * `minimax()`: Implements the Minimax algorithm with Alpha-Beta pruning.
        * `get_best_pacman_action()`: Top-level function to invoke Minimax and select Pac-Man's next move.
    * **Constants:** Define scoring values, penalties, and character representations.

## Future Improvements

* Implement Power Pellet logic (scare ghosts, allow eating ghosts).
* More sophisticated Ghost AI (e.g., Scatter/Chase modes, targeting specific areas, considering other ghosts).
* Graphical interface using libraries like Pygame or Tkinter.
* Different map layouts.
* Implement different AI search algorithms for comparison (e.g., Expectimax for handling probabilistic ghost moves).
* Add sound effects.

## License

`MIT License`
