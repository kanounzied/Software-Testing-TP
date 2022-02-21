from __future__ import annotations

from piece import Piece
import numpy as np
from abc import ABC, abstractmethod
from directions import Directions
from sympy.combinatorics.permutations import Permutation


class Board:
    state = None

    def __init__(self, size: int):

        self.size = size
        self.matrix = np.empty((size, size), dtype=Piece)

        # tab = np.array([3, 1, 2, 4, 5, 0, 6, 7, 8])
        tab = np.array(range(size * size))
        np.random.shuffle(tab)
        while not self.is_solvable(tab):
            np.random.shuffle(tab)
        inter_matrix = tab.reshape(size, size)
        for i in range(size):
            for j in range(size):
                self.matrix[i][j] = Piece((i, j), inter_matrix[i][j], self.size)
        self.transition_to(StateInitial())

    def is_solvable(self, tab: np.array) -> bool:
        permutation_parity = Permutation(tab).signature()
        empty_position = (0, 0)
        mat = tab.reshape(self.size, self.size)
        for i in range(self.size):
            for j in range(self.size):
                if mat[i][j] == 0:
                    empty_position = (i, j)
                    break
        distance = empty_position[0] + empty_position[1]
        empty_parity = 1 if (distance % 2 == 0) else -1
        return empty_parity == permutation_parity

    def update_piece_position(self, x: int, y: int, direction: Directions):  # returns true if the piece has moved
        piece_inter = self.matrix[x + direction.value[0]][y + direction.value[1]]
        if piece_inter.value == 0:
            if self.matrix[x][y].move(direction):
                self.matrix[x + direction.value[0]][y + direction.value[1]] = self.matrix[x][y]
                piece_inter.move(direction.rev())
                self.matrix[x][y] = piece_inter
            else:
                error = "piece in position (" + str(x) + "," + str(y) + ") cannot move to (" + str(
                    x + direction.value[0]) + "," + str(y + direction.value[1]) + ")!"
                raise Exception(error)
        else:
            raise Exception("the selected direction is not empty!")

    def move_up(self):
        self.state.handle_up()

    def move_down(self):
        self.state.handle_down()

    def move_right(self):
        self.state.handle_right()

    def move_left(self):
        self.state.handle_left()

    def find_empty_piece(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j].value == 0: return i, j

    def afficher_pieces(self):
        for i in range(self.size):
            print([j.value for j in self.matrix[i]])

    def get_matrix_numbers(self):
        return [[i.value for i in j] for j in self.matrix]

    def transition_to(self, state: State):
        self.state = state
        self.state.context = self
        # self.afficher_pieces()


class State(ABC):

    @property
    def context(self) -> Board:
        return self._context

    @context.setter
    def context(self, context: Board) -> None:
        self._context = context
        arr = [i.value for i in (np.asarray(context.matrix)).flatten()]

        self.isFinal = np.array_equal(arr, range(context.size * context.size))

        self.empty_position = self.context.find_empty_piece()
        self.left_position = (
            self.empty_position[0] + Directions.Left.value[0], self.empty_position[1] + Directions.Left.value[1])
        self.right_position = (
            self.empty_position[0] + Directions.Right.value[0], self.empty_position[1] + Directions.Right.value[1])
        self.up_position = (
            self.empty_position[0] + Directions.Up.value[0], self.empty_position[1] + Directions.Up.value[1])
        self.down_position = (
            self.empty_position[0] + Directions.Down.value[0], self.empty_position[1] + Directions.Down.value[1])

    @abstractmethod
    def handle_up(self) -> None:
        pass

    @abstractmethod
    def handle_down(self) -> None:
        pass

    @abstractmethod
    def handle_right(self) -> None:
        pass

    @abstractmethod
    def handle_left(self) -> None:
        pass

    def state_matrix_id_gen(self):
        matrix = self.context.matrix
        mat_val = ''.join(''.join('%d' % x.value for x in y) for y in matrix)
        return mat_val


class StateInitial(State):

    def handle_up(self) -> None:
        if self.empty_position[0] == self.context.size - 1:
            print("cannot move up!")
        else:
            position = self.down_position
            self.context.update_piece_position(position[0], position[1], Directions.Up)
            self.context.transition_to(StateUp())

    def handle_down(self) -> None:
        if self.empty_position[0] == 0:
            print("cannot move down!")
        else:
            position = self.up_position
            self.context.update_piece_position(position[0], position[1], Directions.Down)
            self.context.transition_to(StateDown())

    def handle_left(self) -> None:
        if self.empty_position[1] == self.context.size - 1:
            print("cannot move left!")
        else:
            position = self.right_position
            self.context.update_piece_position(position[0], position[1], Directions.Left)
            self.context.transition_to(StateLeft())

    def handle_right(self) -> None:
        if self.empty_position[1] == 0:
            print("cannot move right!")
        else:
            position = self.left_position
            self.context.update_piece_position(position[0], position[1], Directions.Right)
            self.context.transition_to(StateRight())


class StateUp(State):

    def handle_up(self) -> None:
        if self.empty_position[0] == self.context.size - 1:
            print("cannot move up!")
        else:
            position = self.down_position
            self.context.update_piece_position(position[0], position[1], Directions.Up)
            self.context.transition_to(StateUp())

    def handle_down(self) -> None:
        print("won't go back to previous state!")

    def handle_left(self) -> None:
        if self.empty_position[1] == self.context.size - 1:
            print("cannot move left!")
        else:
            position = self.right_position
            self.context.update_piece_position(position[0], position[1], Directions.Left)
            self.context.transition_to(StateLeft())

    def handle_right(self) -> None:
        if self.empty_position[1] == 0:
            print("cannot move right!")
        else:
            position = self.left_position
            self.context.update_piece_position(position[0], position[1], Directions.Right)
            self.context.transition_to(StateRight())


class StateLeft(State):

    def handle_left(self) -> None:
        if self.empty_position[1] == self.context.size - 1:
            print("cannot move left!")
        else:
            position = self.right_position
            self.context.update_piece_position(position[0], position[1], Directions.Left)
            self.context.transition_to(StateLeft())

    def handle_right(self) -> None:
        print("won't go back to previous state!")

    def handle_up(self) -> None:
        if self.empty_position[0] == self.context.size - 1:
            print("cannot move up!")
        else:
            position = self.down_position
            self.context.update_piece_position(position[0], position[1], Directions.Up)
            self.context.transition_to(StateUp())

    def handle_down(self) -> None:
        if self.empty_position[0] == 0:
            print("cannot move down!")
        else:
            position = self.up_position
            self.context.update_piece_position(position[0], position[1], Directions.Down)
            self.context.transition_to(StateDown())


class StateRight(State):

    def handle_right(self) -> None:
        if self.empty_position[1] == 0:
            print("cannot move right!")
        else:
            position = self.left_position
            self.context.update_piece_position(position[0], position[1], Directions.Right)
            self.context.transition_to(StateRight())

    def handle_left(self) -> None:
        print("won't go back to previous state!")

    def handle_up(self) -> None:
        if self.empty_position[0] == self.context.size - 1:
            print("cannot move up!")
        else:
            position = self.down_position
            self.context.update_piece_position(position[0], position[1], Directions.Up)
            self.context.transition_to(StateUp())

    def handle_down(self) -> None:
        if self.empty_position[0] == 0:
            print("cannot move down!")
        else:
            position = self.up_position
            self.context.update_piece_position(position[0], position[1], Directions.Down)
            self.context.transition_to(StateDown())


class StateDown(State):

    def handle_down(self) -> None:
        if self.empty_position[0] == 0:
            print("cannot move down!")
        else:
            position = self.up_position
            self.context.update_piece_position(position[0], position[1], Directions.Down)
            self.context.transition_to(StateDown())

    def handle_up(self) -> None:
        print("won't go back to previous state")

    def handle_right(self) -> None:
        if self.empty_position[1] == 0:
            print("cannot move right!")
        else:
            position = self.left_position
            self.context.update_piece_position(position[0], position[1], Directions.Right)
            self.context.transition_to(StateRight())

    def handle_left(self) -> None:
        if self.empty_position[1] == self.context.size - 1:
            print("cannot move left!")
        else:
            position = self.right_position
            self.context.update_piece_position(position[0], position[1], Directions.Left)
            self.context.transition_to(StateLeft())
