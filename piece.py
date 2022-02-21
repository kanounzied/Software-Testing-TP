from directions import Directions


class Piece:
    coordinates: (int, int)
    value: int
    isEmpty: bool
    size: int

    def __init__(self, coordinates: (int, int), value: int, size: int):
        self.coordinates = coordinates
        self.value = value
        self.size = size
        if value == 0:
            self.isEmpty = True
        else:
            self.isEmpty = False

    def move(self, direction: Directions): # returns true if the piece has moved
        x = self.coordinates[0] + direction.value[0]
        y = self.coordinates[1] + direction.value[1]
        if x in range(self.size) and y in range(self.size):
            # print("moving", self.coordinates, direction.name)
            self.coordinates = (x, y)
        else:
            return False
        return True
