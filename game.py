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


if __name__ == '__main__':
    game = TicTacToe((3, 3))

    state = game.initial_state()
    game.print_state(state)
    while not game.terminal_test(state):
        action = int(input(f'Enter Player 1 action {game.actions(state)}: '))
        state = game.result(state, action)
        game.print_state(state)

        if game.terminal_test(state):
            break

        action = int(input(f'Enter Player 2 action {game.actions(state)}: '))
        state = game.result(state, action)
        game.print_state(state)

    print(
        'Draw' if game.utility(state) == 0 else 'Player 2 win' if game.utility(state) == game.LOSE else 'Player 1 win')
