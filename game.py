from abc import abstractmethod
from functools import cache

Action = int
Player = int
Utility = int
State = tuple[Player, ...]


class Game:
    def __init__(self):
        pass

    @abstractmethod
    def initial_state(self) -> State:
        """
        Returns the initial State of the game
        :return: State
        """
        pass

    @abstractmethod
    def actions(self, state: State) -> tuple[Action, ...]:
        """
        Returns the possible actions from the given State
        :param state: State
        :return: tuple[Action, ...]
        """
        pass

    @abstractmethod
    def result(self, state: State, action: Action) -> State:
        """
        Returns the resulting State after applying the given Action to the given State
        :param state: State
        :param action: Action
        :return: State after applying the given Action
        """
        pass

    @abstractmethod
    def utility(self, state: State, player: Player) -> Utility:
        """
        Returns the Utility of the given State for the given Player
        :param state: State
        :param player: Player
        :return: Utility of the given State for the given Player
        """
        pass

    @abstractmethod
    def terminal_test(self, state: State) -> bool:
        """
        Returns True if the game is over
        :param state: State
        :return: True if the game is over
        """
        pass


class TicTacToe(Game):
    """
    Tic-Tac-Toe game
    """
    X: Player = 1
    O: Player = -1
    EMPTY: Player = 0

    WIN: Utility = 1
    LOSE: Utility = -1
    DRAW: Utility = 0

    def __init__(self, size: tuple[int, int] = (3, 3)):
        super().__init__()
        self.height, self.width = size

    def initial_state(self) -> State:
        return tuple(self.EMPTY for _ in range(self.height * self.width))

    @cache
    def actions(self, state: State) -> tuple[Action, ...]:
        return tuple(i for i, v in enumerate(state) if v == self.EMPTY)

    @cache
    def result(self, state: State, action: Action) -> State:
        new_state = list(state)
        player_ = self.O if new_state.count(self.X) > new_state.count(self.O) else self.X
        new_state[action] = player_
        return tuple(new_state)

    @cache
    def all_same(self, state: State) -> bool:
        return len(set(state)) == 1

    @cache
    def utility(self, state: State, player: Player = X) -> Utility:
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
    def terminal_test(self, state: State) -> bool:
        return len(self.actions(state)) == 0 or self.utility(state) != self.DRAW

    def print_state(self, state: State):
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
        action = int(input(f'Enter Player 1 Action {game.actions(state)}: '))
        state = game.result(state, action)
        game.print_state(state)

        if game.terminal_test(state):
            break

        action = int(input(f'Enter Player 2 Action {game.actions(state)}: '))
        state = game.result(state, action)
        game.print_state(state)

    print(
        'Draw' if game.utility(state) == 0 else 'Player 2 win' if game.utility(state) == game.LOSE else 'Player 1 win')
