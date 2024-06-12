# Tic-Tac-Toe with AI Strategies

This Python project implements a Tic-Tac-Toe game with various strategies for AI players. The strategies include Min-Max, Heuristic, and Alpha-Beta pruning. The game can be played between two AI players, between a human and an AI, or between two humans.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Classes and Methods](#classes-and-methods)
- [License](#license)

## Installation

To run this project, you need to have Python installed on your machine. You can clone the repository and run the scripts directly.

```bash
git clone https://github.com/flateon/tic-tac-toe.git
cd tic-tac-toe
```

## Usage

To start the game, run the `strategy.py` script:

```bash
python strategy.py
```

You will be prompted to choose strategies for Player 1 and Player 2. The available strategies are:

- `0` - MinMax
- `1` - Heuristic
- `2` - AlphaBeta
- `3` - Human

For example, to play a game between Heuristic and AlphaBeta strategy:

```
The strategy for Player 1 (0 - MinMax, 1 - Heuristic, 2 - AlphaBeta, 3 - Human): 1
The strategy for Player 2 (0 - MinMax, 1 - Heuristic, 2 - AlphaBeta, 3 - Human): 2
 | | 
-----
 |X| 
-----
 | | 


O| | 
-----
 |X| 
-----
 | | 


O| | 
-----
 |X|X
-----
 | | 


O| | 
-----
O|X|X
-----
 | | 


O| | 
-----
O|X|X
-----
X| | 


O| |O
-----
O|X|X
-----
X| | 


O|X|O
-----
O|X|X
-----
X| | 


O|X|O
-----
O|X|X
-----
X|O| 


O|X|O
-----
O|X|X
-----
X|O|X


Draw
AI 1 Evaluated 773 leaf nodes
AI 2 Evaluated 197 leaf nodes
Time: 54.43 ms
```

## Classes and Methods

### `game.py`

- **Game**: Abstract base class defining the game structure.
  - `initial_state()`: Returns the initial state of the game.
  - `actions(state)`: Returns possible actions from the given state.
  - `result(state, action)`: Returns the resulting state after applying the given action.
  - `utility(state, player)`: Returns the utility of the given state for the given player.
  - `terminal_test(state)`: Returns True if the game is over.

- **TicTacToe**: Implements the Tic-Tac-Toe game.
  - `__init__(size=(3, 3))`: Initializes the game with a given board size.
  - `initial_state()`: Returns the initial empty board state.
  - `actions(state)`: Returns the list of valid actions (empty cells).
  - `result(state, action)`: Returns the new state after a move.
  - `utility(state, player)`: Evaluates the board and returns the utility.
  - `terminal_test(state)`: Checks if the game has ended.
  - `print_state(state)`: Prints the current state of the board.

### `strategy.py`

- **Strategy**: Abstract base class for strategies.
  - `action(state, player)`: Returns the best action for the given state and player.
  - `evaluation(state, player)`: Evaluates the state for the given player.

- **Human**: Strategy for a human player.
  - `action(state, player)`: Prompts the human player for a move.

- **MinMax**: Implements the Min-Max strategy.
  - `evaluation(state, player)`: Evaluates the state.
  - `max_value(state, player)`: Returns the max value for the Min-Max algorithm.
  - `min_value(state, player)`: Returns the min value for the Min-Max algorithm.

- **Heuristic**: Implements a heuristic-based strategy.
  - `heuristic(state, player)`: Heuristic function to evaluate the state.
  - `max_value(state, player, depth)`: Returns the max value with depth limitation.
  - `min_value(state, player, depth)`: Returns the min value with depth limitation.

- **AlphaBeta**: Implements the Alpha-Beta pruning strategy.
  - `max_value(state, player, depth, alpha, beta)`: Returns the max value with Alpha-Beta pruning.
  - `min_value(state, player, depth, alpha, beta)`: Returns the min value with Alpha-Beta pruning.

## License

This project is licensed under the MIT License. 