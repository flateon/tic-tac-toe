from abc import abstractmethod
from array import array

state = array
action = int
player = int
utility = int


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
        return array('b', [self.EMPTY] * self.height * self.width)

    def actions(self, state: state) -> tuple[action, ...]:
        return tuple(i for i, v in enumerate(state) if v == self.EMPTY)

    def result(self, state: state, action: action) -> state:
        new_state = state[:]
        player_ = self.O if state.count(self.X) > state.count(self.O) else self.X
        new_state[action] = player_
        return new_state

    def all_same(self, state: state) -> bool:
        return len(set(state)) == 1
        # return all(state[i] == state[0] for i in range(len(state)))

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

    def terminal_test(self, state: state) -> bool:
        return len(self.actions(state)) == 0 or self.utility(state) != self.DRAW

    def print_state(self, state: state):
        to_str = {self.X: 'X', self.O: 'O', self.EMPTY: ' '}
        for i in range(self.height):
            print('|'.join(to_str[state[i * self.width + j]] for j in range(self.width)))
            if i != self.height - 1:
                print('-' * (self.width * 2 - 1))
        print('#' * 30)


class MinMax(TicTacToe):
    def __init__(self, size: tuple[int, int] = (3, 3)):
        super().__init__(size)
        self.num_utility = 0

    def utility(self, state: state, player: player = TicTacToe.X) -> utility:
        self.num_utility += 1
        return super().utility(state, player)

    def minimax(self, state: state, player: player) -> action:
        value = [self.min_value(self.result(state, a), player) for a in self.actions(state)]
        return self.actions(state)[value.index(max(value))]

    def max_value(self, state: state, player: player) -> int:
        if self.terminal_test(state):
            return self.utility(state, player)
        value = [self.min_value(self.result(state, a), player) for a in self.actions(state)]
        return max(value)

    def min_value(self, state: state, player: player) -> int:
        if self.terminal_test(state):
            return self.utility(state, player)
        value = [self.max_value(self.result(state, a), player) for a in self.actions(state)]
        return min(value)


if __name__ == '__main__':
    game = MinMax((3, 3))
    state = game.initial_state()
    while not game.terminal_test(state):
        action = game.minimax(state, game.X)
        state = game.result(state, action)
        game.print_state(state)

        if game.terminal_test(state):
            break
        # action = int(input(f'Enter your move {game.actions(state)}: '))
        action = game.minimax(state, game.O)
        state = game.result(state, action)
        game.print_state(state)
    print('Draw' if game.utility(state) == 0 else 'You lose' if game.utility(state) == 10 else 'You win')
    print(game.num_utility)
