import time
from abc import abstractmethod
from functools import cache

from game import Game, State, Player, Action, Utility, TicTacToe


class Strategy:
    def __init__(self, game: Game):
        self.game = game
        self.num_leafs = 0

    def __getattr__(self, item):
        return getattr(self.game, item)

    @abstractmethod
    def action(self, state: State, player: Player) -> Action:
        """
        Returns the best Action for the given State and Player
        :param state:
        :param player:
        :return: best Action for the given State and Player
        """
        pass

    def evaluation(self, state: State, player: Player) -> Utility:
        """
        Returns the Utility of the given State for the given Player
        :param state:
        :param player:
        :return: Utility of the given State for the given Player
        """
        pass


class Human(Strategy):
    def action(self, state: State, player: Player) -> Action:
        return int(input(f'Enter your action {game.actions(state)}: '))


class MinMax(Strategy):
    def evaluation(self, state: State, player: Player) -> Utility:
        self.num_leafs += 1
        return self.utility(state, player)

    def action(self, state: State, player: Player) -> Action:
        value = [self.min_value(self.result(state, a), player) for a in self.actions(state)]
        return self.actions(state)[value.index(max(value))]

    def max_value(self, state: State, player: Player) -> int:
        if self.terminal_test(state):
            return self.evaluation(state, player)
        value = [self.min_value(self.result(state, a), player) for a in self.actions(state)]
        return max(value)

    def min_value(self, state: State, player: Player) -> int:
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
    def possible_winning_lines(self, state: State, player: Player) -> int:
        """
        Returns the number of possible winning lines for the given Player
        :param state: State
        :param player: Player
        :return: number of possible winning lines for the given Player
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
    def heuristic(self, state: State, player: Player) -> Utility:
        """
        Heuristic function
        :param state: State
        :param player: Player
        :return: heuristic value
        """
        if self.terminal_test(state):
            return self.utility(state, player) * 100
        else:
            return self.possible_winning_lines(state, player) - self.possible_winning_lines(state, -player)

    def evaluation(self, state: State, player: Player) -> Utility:
        self.num_leafs += 1
        return self.heuristic(state, player)

    def action(self, state: State, player: Player) -> Action:
        value = [self.min_value(self.result(state, a), player, self.depth - 1) for a in self.actions(state)]
        return self.actions(state)[value.index(max(value))]

    def max_value(self, state: State, player: Player, depth: int) -> int:
        if depth == 0 or self.terminal_test(state):
            return self.evaluation(state, player)
        value = [self.min_value(self.result(state, a), player, depth - 1) for a in self.actions(state)]
        return max(value)

    def min_value(self, state: State, player: Player, depth: int) -> int:
        if depth == 0 or self.terminal_test(state):
            return self.evaluation(state, player)
        value = [self.max_value(self.result(state, a), player, depth - 1) for a in self.actions(state)]
        return min(value)


class AlphaBeta(Heuristic):
    def __init__(self, game: Game, depth: int = 3):
        super().__init__(game, depth)

    def action(self, state: State, player: Player) -> Action:
        value = [self.min_value(self.result(state, a), player, self.depth - 1, -float('inf'), float('inf'))
                 for a in self.actions(state)]
        return self.actions(state)[value.index(max(value))]

    def max_value(self, state: State, player: Player, depth: int, alpha: float, beta: float) -> int:
        if depth == 0 or self.terminal_test(state):
            return self.evaluation(state, player)
        v = -float('inf')
        for a in self.actions(state):
            v = max(v, self.min_value(self.result(state, a), player, depth - 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state: State, player: Player, depth: int, alpha: float, beta: float) -> int:
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

    strategies = {
        '0': MinMax,
        '1': Heuristic,
        '2': AlphaBeta,
        '3': Human,
    }
    ai_1 = strategies.get(input('The strategy for Player 1 (0 - MinMax, 1 - Heuristic, 2 - AlphaBeta, 3 - Human):'), AlphaBeta)(game)
    ai_2 = strategies.get(input('The strategy for Player 2 (0 - MinMax, 1 - Heuristic, 2 - AlphaBeta, 3 - Human):'), AlphaBeta)(game)

    state = game.initial_state()
    start = time.time()
    while not game.terminal_test(state):
        action = ai_1.action(state, game.X)
        state = game.result(state, action)
        game.print_state(state)

        if game.terminal_test(state):
            break

        action = ai_2.action(state, game.O)
        state = game.result(state, action)
        game.print_state(state)

    print(
        'Draw' if game.utility(state) == 0 else 'Player 2 win' if game.utility(state) == game.LOSE else 'Player 1 win')
    print(f'AI 1 Evaluated {ai_1.num_leafs} leaf nodes')
    print(f'AI 2 Evaluated {ai_2.num_leafs} leaf nodes')
    print(f'Time: {(time.time() - start) * 1000:.2f} ms')
