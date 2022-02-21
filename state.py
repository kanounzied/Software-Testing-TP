from __future__ import annotations
import numpy as np
from abc import ABC, abstractmethod

from board import Board
from directions import Directions


class State(ABC):

    isFinal = False

    @property
    def context(self) -> Board:
        return self._context

    @context.setter
    def context(self, context: Board) -> None:
        self._context = context
        arr = [i.value for i in (np.asarray(context.matrix)).flatten()]
        self.isFinal = np.array_equal(arr, range(context.size * context.size))
        self.empty_position = self.context.find_empty_piece()
        self.left_position = (self.empty_position[0] + Directions.Left[0], self.empty_position[1] + Directions.Left[1])
        self.right_position = (
            self.empty_position[0] + Directions.Right[0], self.empty_position[1] + Directions.Right[1])
        self.up_position = (self.empty_position[0] + Directions.Up[0], self.empty_position[1] + Directions.Up[1])
        self.down_position = (self.empty_position[0] + Directions.Down[0], self.empty_position[1] + Directions.Down[1])

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


class StateInitial(State):

    def handle_up(self) -> None:
        if self.empty_position[0] == 2:
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
        if self.empty_position[1] == 2:
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
        if self.empty_position[0] == 2:
            print("cannot move up!")
        else:
            position = self.down_position
            self.context.update_piece_position(position[0], position[1], Directions.Up)
            self.context.transition_to(StateUp())

    def handle_down(self) -> None:
        pass
        # print("won't go back to previous state!")

    def handle_left(self) -> None:
        if self.empty_position[1] == 2:
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
            self.context.transition_to( ())


class StateLeft(State):

    def handle_left(self) -> None:
        if self.empty_position[1] == 2:
            print("cannot move left!")
        else:
            position = self.right_position
            self.context.update_piece_position(position[0], position[1], Directions.Left)
            self.context.transition_to(StateLeft())

    def handle_right(self) -> None:
        pass
        # print("won't go back to previous state!")

    def handle_up(self) -> None:
        if self.empty_position[0] == 2:
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
        pass
        # print("won't go back to previous state!")

    def handle_up(self) -> None:
        if self.empty_position[0] == 2:
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
        pass
        # print("won't go back to previous state")

    def handle_right(self) -> None:
        if self.empty_position[1] == 0:
            print("cannot move right!")
        else:
            position = self.left_position
            self.context.update_piece_position(position[0], position[1], Directions.Right)
            self.context.transition_to(StateRight())

    def handle_left(self) -> None:
        if self.empty_position[1] == 2:
            print("cannot move left!")
        else:
            position = self.right_position
            self.context.update_piece_position(position[0], position[1], Directions.Left)
            self.context.transition_to(StateLeft())
