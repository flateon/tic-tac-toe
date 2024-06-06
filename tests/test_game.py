import unittest
from array import array

from game import TicTacToe


# 单元测试类
class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe()  # 假设是一个3x3的游戏盘面

    def get_state(self, state: list[str]):
        str2state = {
            'X': self.game.X,
            'O': self.game.O,
            ' ': self.game.EMPTY
        }
        return tuple(str2state[c] for c in state)

    def test_win_horizontal(self):
        state = [
            self.get_state(['X', 'X', 'X',
                            'O', 'O', 'X',
                            ' ', ' ', ' ', ]),
            self.get_state(['O', 'X', 'O',
                            'X', 'X', 'X',
                            ' ', ' ', ' ', ]),
            self.get_state([' ', ' ', ' ',
                            'X', 'O', 'O',
                            'X', 'X', 'X', ]),
        ]
        for state in state:
            self.assertEqual(self.game.utility(state), self.game.WIN)

    def test_win_vertical(self):
        state = [
            self.get_state(['X', 'O', ' ',
                            'X', 'O', ' ',
                            'X', ' ', 'O']),
            self.get_state(['O', 'X', ' ',
                            'O', 'X', ' ',
                            ' ', 'X', 'O']),
            self.get_state([' ', ' ', 'X',
                            'O', 'O', 'X',
                            ' ', ' ', 'X']),
        ]
        for state in state:
            self.assertEqual(self.game.utility(state), self.game.WIN)

    def test_win_diagonal(self):
        state = [
            self.get_state(['X', 'O', ' ',
                            'O', 'X', ' ',
                            ' ', ' ', 'X']),
            self.get_state([' ', ' ', 'X',
                            'O', 'X', ' ',
                            'X', 'O', ' ']),
        ]
        for state in state:
            self.assertEqual(self.game.utility(state), self.game.WIN)

    def test_loss_horizontal(self):
        state = [
            self.get_state(['O', 'O', 'O',
                            'X', 'X', ' ',
                            ' ', ' ', ' ']),
            self.get_state(['X', ' ', ' ',
                            'O', 'O', 'O',
                            'X', 'X', ' ']),
            self.get_state([' ', ' ', ' ',
                            'X', 'X', ' ',
                            'O', 'O', 'O']),
        ]
        for state in state:
            self.assertEqual(self.game.utility(state), self.game.LOSE)

    def test_loss_vertical(self):
        state = [
            self.get_state(['O', 'X', ' ',
                            'O', 'X', ' ',
                            'O', ' ', 'X']),
            self.get_state(['X', 'O', ' ',
                            'X', 'O', ' ',
                            ' ', 'O', 'X']),
            self.get_state([' ', ' ', 'O',
                            'X', 'X', 'O',
                            ' ', ' ', 'O']),
        ]
        for state in state:
            self.assertEqual(self.game.utility(state), self.game.LOSE)

    def test_loss_diagonal(self):
        state = [
            self.get_state(['O', 'X', ' ',
                            'X', 'O', ' ',
                            ' ', ' ', 'O']),
            self.get_state([' ', ' ', 'O',
                            'X', 'O', ' ',
                            'O', 'X', ' ']),
        ]
        for state in state:
            self.assertEqual(self.game.utility(state), self.game.LOSE)

    def test_draw(self):
        state = [
            self.get_state(['X', 'O', 'X',
                            'X', 'O', 'O',
                            'O', 'X', 'X']),
            self.get_state(['O', 'X', 'O',
                            'O', 'X', 'X',
                            'X', 'O', 'O']),
            self.get_state(['X', 'X', 'O',
                            'O', 'O', 'X',
                            'X', 'O', 'X']),
        ]
        for state in state:
            self.assertEqual(self.game.utility(state), self.game.DRAW)


if __name__ == '__main__':
    unittest.main()
