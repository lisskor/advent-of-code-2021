import sys
import numpy as np


def read_input(filename: str):
    with open(filename, 'r', encoding='utf8') as fh:
        lines = [[[int(coord)
                   for coord in point.split(',')]
                  for point in line.strip().split(' -> ')]
                 for line in fh]
    return np.array(lines, dtype=int)


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class VentLine:
    def __init__(self, coords: list[list[int]]):
        self.x1, self.y1 = coords[0]
        self.x2, self.y2 = coords[1]

        self.max_x = self.x1 if self.x1 > self.x2 else self.x2
        self.min_x = self.x2 if self.max_x == self.x1 else self.x1
        self.max_y = self.y1 if self.y1 > self.y2 else self.y2
        self.min_y = self.y2 if self.max_y == self.y1 else self.y1

        self.horizontal = True if self.y1 == self.y2 else False
        self.vertical = True if self.x1 == self.x2 else False
        self.diagonal = True if self.x1 != self.x2 and self.y1 != self.y2 else False

        self.points = self.generate_points_on_line()

    def __repr__(self):
        return f"{self.x1},{self.y1}->{self.x2},{self.y2}"

    def generate_points_on_line(self):
        points = []

        if self.horizontal:
            points = [[x, self.y1] for x in np.arange(self.min_x, self.max_x + 1, 1)]
        elif self.vertical:
            points = [[self.x1, y] for y in np.arange(self.min_y, self.max_y + 1, 1)]
        elif self.diagonal:
            xs = np.arange(self.x1, self.x2 + 1, 1) if self.x1 < self.x2 else np.arange(self.x1, self.x2 - 1, -1)
            ys = np.arange(self.y1, self.y2 + 1, 1) if self.y1 < self.y2 else np.arange(self.y1, self.y2 - 1, -1)
            points = list(zip(xs, ys))
        return points


class VentMap:
    def __init__(self, max_coord: int):
        self.map = np.zeros((max_coord, max_coord), dtype=int)
        self.overlaps = (self.map > 1).sum()

    def __repr__(self):
        out_string = str(self.map)
        return out_string

    def add_line(self, line: VentLine):
        for point in line.points:
            self.map[point[0], point[1]] += 1
        self.overlaps = (self.map > 1).sum()


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    vent_lines = []
    input_lines = read_input(input_file)
    if part == "1":
        for input_line in input_lines:
            if not VentLine(input_line).diagonal:
                vent_lines.append(VentLine(input_line))
    elif part == "2":
        for input_line in input_lines:
            vent_lines.append(VentLine(input_line))

    vent_map = VentMap(input_lines.max()+1)

    for vent_line in vent_lines:
        vent_map.add_line(vent_line)

    print("Got this map:")
    print(vent_map)
    print(f"There are {vent_map.overlaps} points where lines overlap")
