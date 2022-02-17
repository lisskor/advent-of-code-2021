import sys
import numpy as np


def read_input(filename: str):
    points = []
    instructions = []
    with open(filename, 'r', encoding='utf8') as fh:
        for line in fh:
            if line.startswith("fold along"):
                instructions.append(line.strip().split(' ')[2].split('='))
            elif len(line) > 1:
                x, y = line.strip().split(',')
                points.append((int(x), int(y)))
    return points, instructions


class TransparentMap:
    def __init__(self, points: list[tuple[int, int]]):
        self.width = max([coords[0] for coords in points]) + 1
        self.height = max([coords[1] for coords in points]) + 1

        self.map = np.zeros((self.height, self.width), dtype=int)
        # print(self.map.shape)

        for point in points:
            self.map[point[1], point[0]] = 1

    def fold_up(self, y: int):
        # print(self.height - 2*(self.height - (y + 1)) -1 )
        self.map[:y, :] += self.map[y+1:, :][::-1, :]
        self.map = np.clip(self.map[:y, :], a_min=0, a_max=1)
        self.width, self.height = self.map.shape

    # def fold_up(self, y: int):
    #     bottom_half = self.map[y+1:, :][::-1, :]
    #     top_half = self.map[:y, :]
    #     if bottom_half.shape[0] <= top_half.shape[0]:
    #         # if bottom part is smaller, put bottom over top
    #         result = top_half
    #
    #     else:
    #         # if top part is smaller, put top over bottom
    #         pass
    #     if self.height // 2 == 1:
    #         print("old up")
    #         self.map[:y, :] += self.map[y+1:, :][::-1, :]
    #         self.map = np.clip(self.map[:y, :], a_min=0, a_max=1)
    #     else:
    #         print("new up")
    #         self.map[:y+1, :] += self.map[y:, :][::-1, :]
    #         self.map = np.clip(self.map[:y+1, :], a_min=0, a_max=1)
    #     self.width, self.height = self.map.shape

    def fold_left(self, x: int):
        # print(self.width - 2*(self.width - (x + 1)) - 1)
        self.map[:, :x] += self.map[:, x+1:][:, ::-1]
        self.map = np.clip(self.map[:, :x], a_min=0, a_max=1)
        self.width, self.height = self.map.shape

    # def fold_left(self, x: int):
    #     right_half = self.map[:, x+1:][:, ::-1]
    #     left_half = self.map[:, :x]
    #     if self.width // 2 == 1:
    #         print("old left")
    #         self.map[:, :x] += self.map[:, x+1:][:, ::-1]
    #         self.map = np.clip(self.map[:, :x], a_min=0, a_max=1)
    #     else:
    #         print("new left")
    #         self.map[:, :x+1] += self.map[:, x:][:, ::-1]
    #         self.map = np.clip(self.map[:, :x+1], a_min=0, a_max=1)
    #     self.width, self.height = self.map.shape


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    inp_points, inp_instr = read_input(input_file)
    transparent_map = TransparentMap(inp_points)
    if part == "1":
        for direction, value in inp_instr[:1]:
            if direction == "x":
                transparent_map.fold_left(int(value))
            elif direction == "y":
                transparent_map.fold_up(int(value))
        print("Visible dots:", transparent_map.map.sum())
    # elif part == "2":
    #     for direction, value in inp_instr:
    #         if direction == "x":
    #             print(f"shape {transparent_map.map.shape}, fold left at x={value}")
    #             transparent_map.old_fold_left(int(value))
    #         elif direction == "y":
    #             print(f"shape {transparent_map.map.shape}, fold up at y={value}")
    #             transparent_map.old_fold_up(int(value))
    #     print(transparent_map.map)
