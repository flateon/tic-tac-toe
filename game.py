import time
from abc import abstractmethod
from functools import cache

action = int
player = int
utility = int
state = tuple[player, ...]


class Game:
    def __init__(self):
        pass

    @abstractmethod
    def initial_state(self) -> state:
        """
        Returns the initial state of the game
        :return: state
        """
        pass

    @abstractmethod
    def actions(self, state: state) -> tuple[action, ...]:
        """
        Returns the possible actions from the given state
        :param state: state
        :return: tuple[action, ...]
        """
        pass

    @abstractmethod
    def result(self, state: state, action: action) -> state:
        """
        Returns the resulting state after applying the given action to the given state
        :param state: state
        :param action: action
        :return: state after applying the given action
        """
        pass

    @abstractmethod
    def utility(self, state: state, player: player) -> utility:
        """
        Returns the utility of the given state for the given player
        :param state: state
        :param player: player
        :return: utility of the given state for the given player
        """
        pass

    @abstractmethod
    def terminal_test(self, state: state) -> bool:
        """
        Returns True if the game is over
        :param state: state
        :return: True if the game is over
        """
        pass


class TicTacToe(Game):
    """
    Tic-Tac-Toe game
    """
    X: player = 1
    O: player = -1
    EMPTY: player = 0

    WIN: utility = 1
    LOSE: utility = -1
    DRAW: utility = 0

    def __init__(self, size: tuple[int, int] = (3, 3)):
        super().__init__()
        self.height, self.width = size

    def initial_state(self) -> state:
        return tuple(self.EMPTY for _ in range(self.height * self.width))

    @cache
    def actions(self, state: state) -> tuple[action, ...]:
        return tuple(i for i, v in enumerate(state) if v == self.EMPTY)

    @cache
    def result(self, state: state, action: action) -> state:
        new_state = list(state)
        player_ = self.O if new_state.count(self.X) > new_state.count(self.O) else self.X
        new_state[action] = player_
        return tuple(new_state)

    @cache
    def all_same(self, state: state) -> bool:
        return len(set(state)) == 1

    @cache
    def utility(self, state: state, player: player = X) -> utility:
        for i in range(self.height):
            if self.all_same(state[i * self.width: (i + 1) * self.width]):
                if state[i * self.width] == player:
                    return self.WIN
                elif state[i * self.width] != self.EMPTY:
                    return self.LOSE

        for i in range(self.width):
            if self.all_same(state[i::self.width]):
                if state[i] == player:
                    return self.WIN
                elif state[i] != self.EMPTY:
                    return self.LOSE

        if self.all_same(state[::self.width + 1]):
            if state[0] == player:
                return self.WIN
            elif state[0] != self.EMPTY:
                return self.LOSE

        if self.all_same(state[self.width - 1:-1:self.width - 1]):
            if state[self.width - 1] == player:
                return self.WIN
            elif state[self.width - 1] != self.EMPTY:
                return self.LOSE

        return self.DRAW

    @cache
    def terminal_test(self, state: state) -> bool:
        return len(self.actions(state)) == 0 or self.utility(state) != self.DRAW

    def print_state(self, state: state):
        to_str = {self.X: 'X', self.O: 'O', self.EMPTY: ' '}
        for i in range(self.height):
            print('|'.join(to_str[state[i * self.width + j]] for j in range(self.width)))
            if i != self.height - 1:
                print('-' * (self.width * 2 - 1))
        print('\n')


class Strategy:
    def __init__(self, game: Game):
        self.game = game
        self.num_leafs = 0

    def __getattr__(self, item):
        return getattr(self.game, item)

    @abstractmethod
    def action(self, state: state, player: player) -> action:
        """
        Returns the best action for the given state and player
        :param state:
        :param player:
        :return: best action for the given state and player
        """
        pass

    @abstractmethod
    def evaluation(self, state: state, player: player) -> utility:
        """
        Returns the utility of the given state for the given player
        :param state:
        :param player:
        :return: utility of the given state for the given player
        """
        pass


class MinMax(Strategy):
    def evaluation(self, state: state, player: player) -> utility:
        self.num_leafs += 1
        return self.utility(state, player)

    def action(self, state: state, player: player) -> action:
        value = [self.min_value(self.result(state, a), player) for a in self.actions(state)]
        return self.actions(state)[value.index(max(value))]

    def max_value(self, state: state, player: player) -> int:
        if self.terminal_test(state):
            return self.evaluation(state, player)
        value = [self.min_value(self.result(state, a), player) for a in self.actions(state)]
        return max(value)

    def min_value(self, state: state, player: player) -> int:
        if self.terminal_test(state):
            return self.evaluation(state, player)
        value = [self.max_value(self.result(state, a), player) for a in self.actions(state)]
        return min(value)


class Heuristic(Strategy):
    def __init__(self, game: Game, depth: int = 3):
        """
        :param game: game
        :param depth: depth of the search
        """
        super().__init__(game)
        self.depth = depth

    @cache
    def possible_winning_lines(self, state: state, player: player) -> int:
        """
        Returns the number of possible winning lines for the given player
        :param state: state
        :param player: player
        :return: number of possible winning lines for the given player
        """
        best_state = tuple(player if i == self.EMPTY else i for i in state)
        cnt = 0
        for i in range(self.height):
            if best_state[i * self.width] == player and self.all_same(best_state[i * self.width: (i + 1) * self.width]):
                cnt += 1

        for i in range(self.width):
            if best_state[i] == player and self.all_same(best_state[i::self.width]):
                cnt += 1

        if best_state[0] == player and self.all_same(best_state[::self.width + 1]):
            cnt += 1

        if best_state[self.width - 1] and self.all_same(best_state[self.width - 1:-1:self.width - 1]):
            cnt += 1

        return cnt

    @cache
    def heuristic(self, state: state, player: player) -> utility:
        """
        Heuristic function
        :param state: state
        :param player: player
        :return: heuristic value
        """
        if self.terminal_test(state):
            return self.utility(state, player) * 100
        else:
            return self.possible_winning_lines(state, player) - self.possible_winning_lines(state, -player)

    def evaluation(self, state: state, player: player) -> utility:
        self.num_leafs += 1
        return self.heuristic(state, player)

    def action(self, state: state, player: player) -> action:
        value = [self.min_value(self.result(state, a), player, self.depth - 1) for a in self.actions(state)]
        return self.actions(state)[value.index(max(value))]

    def max_value(self, state: state, player: player, depth: int) -> int:
        if depth == 0 or self.terminal_test(state):
            return self.evaluation(state, player)
        value = [self.min_value(self.result(state, a), player, depth - 1) for a in self.actions(state)]
        return max(value)

    def min_value(self, state: state, player: player, depth: int) -> int:
        if depth == 0 or self.terminal_test(state):
            return self.evaluation(state, player)
        value = [self.max_value(self.result(state, a), player, depth - 1) for a in self.actions(state)]
        return min(value)


class AlphaBeta(Heuristic):
    def __init__(self, game: Game, depth: int = 3):
        super().__init__(game, depth)

    def action(self, state: state, player: player) -> action:
        value = [self.min_value(self.result(state, a), player, self.depth - 1, -float('inf'), float('inf'))
                 for a in self.actions(state)]
        return self.actions(state)[value.index(max(value))]

    def max_value(self, state: state, player: player, depth: int, alpha: float, beta: float) -> int:
        if depth == 0 or self.terminal_test(state):
            return self.evaluation(state, player)
        v = -float('inf')
        for a in self.actions(state):
            v = max(v, self.min_value(self.result(state, a), player, depth - 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state: state, player: player, depth: int, alpha: float, beta: float) -> int:
        if depth == 0 or self.terminal_test(state):
            return self.evaluation(state, player)
        v = float('inf')
        for a in self.actions(state):
            v = min(v, self.max_value(self.result(state, a), player, depth - 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


if __name__ == '__main__':
    game = TicTacToe((3, 3))

    ai = AlphaBeta(game, 3)
    # ai = Heuristic(game, 3)
    # ai = MinMax(game)

    state = game.initial_state()
    start = time.time()
    while not game.terminal_test(state):
        # action = int(input(f'Enter your move {game.actions(state)}: '))
        action = ai.action(state, game.X)
        state = game.result(state, action)
        game.print_state(state)

        if game.terminal_test(state):
            break

        action = ai.action(state, game.O)
        state = game.result(state, action)
        game.print_state(state)

    print('Draw' if game.utility(state) == 0 else 'You lose' if game.utility(state) == game.LOSE else 'You win')
    print(f'Evaluated {ai.num_leafs} leaf nodes')
    print(f'{(time.time() - start) * 1000:.2f} ms')
