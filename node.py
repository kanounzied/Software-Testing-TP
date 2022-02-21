from board import Board
import copy


class Node:

    def __init__(self, board: Board):
        self.board = board
        self._up = None
        self._down = None
        self._left = None
        self._right = None
        self.cost = 0

    @property
    def up(self):
        if self._up is None:
            new_board = copy.deepcopy(self.board)
            new_board.move_up()
            self._up = Node(new_board)
        return self._up

    @property
    def down(self):
        if self._down is None:
            new_board = copy.deepcopy(self.board)
            new_board.move_down()
            self._down = Node(new_board)
        return self._down

    @property
    def left(self):
        if self._left is None:
            new_board = copy.deepcopy(self.board)
            new_board.move_left()
            self._left = Node(new_board)
        return self._left

    @property
    def right(self):
        if self._right is None:
            new_board = copy.deepcopy(self.board)
            new_board.move_right()
            self._right = Node(new_board)
        return self._right
