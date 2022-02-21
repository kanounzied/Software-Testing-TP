import enum


class Directions(enum.Enum):
    Left = (0, -1)
    Down = (1, 0)
    Right = (0, 1)
    Up = (-1, 0)

    def rev(self):
        if self.name == "Up": return self.Down
        if self.name == "Down": return self.Up
        if self.name == "Right": return self.Left
        if self.name == "Left": return self.Right
