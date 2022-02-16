import sys
import numpy as np


def read_input(filename: str):
    with open(filename, 'r', encoding='utf8') as fh:
        lines = [[int(ch) for ch in line.strip()] for line in fh]
    return np.array(lines, dtype=int)


def neighbor_indices(x: int, y: int):
    indices = [(x - 1, y),
               (x + 1, y),
               (x, y - 1),
               (x, y + 1)]
    return indices


class HeightMap:
    def __init__(self, heights: np.array):
        self.map = heights
        self.rows, self.columns = self.map.shape
        self.padded_map = np.full((self.rows+2, self.columns+2), 10)
        self.padded_map[1:-1, 1:-1] = self.map
        self.low_points = np.array([[self.is_low_point(row, col)
                                     for col in range(1, self.padded_map.shape[1]-1)]
                                    for row in range(1, self.padded_map.shape[0]-1)])
        self.risk_level = (self.map * self.low_points).sum() + self.low_points.sum()
        self.discovered = np.zeros_like(self.padded_map)

        self.basin_sizes = []
        for point in np.argwhere(self.low_points > 0):
            # get a counter for discovered nodes
            self.current_counter = 0
            # in coordinates of padded map
            x = point[0] + 1
            y = point[1] + 1
            self.dfs(x, y)
            self.basin_sizes.append(self.current_counter)
        # reset counter
        self.current_counter = 0

    def __repr__(self):
        out_string = str(self.map)
        return out_string

    def is_low_point(self, x: int, y: int):
        neighbors = [self.padded_map[x-1, y],
                     self.padded_map[x+1, y],
                     self.padded_map[x, y-1],
                     self.padded_map[x, y+1]]
        if sum([self.padded_map[x, y] < n for n in neighbors]) == 4:
            return 1
        else:
            return 0

    def adjacent_nodes(self, x: int, y: int):
        return [n for n in neighbor_indices(x, y) if self.padded_map[n] < 9]

    def dfs(self, start_x: int, start_y: int):
        self.discovered[start_x, start_y] = 1
        self.current_counter += 1
        for point in self.adjacent_nodes(start_x, start_y):
            if self.discovered[point] == 0:
                self.dfs(point[0], point[1])


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    height_map = HeightMap(read_input(input_file))
    if part == "1":
        print("Total risk level:", height_map.risk_level)
    elif part == "2":
        all_sizes = height_map.basin_sizes
        all_sizes.sort(reverse=True)
        print("Sizes of 3 largest basins multiplied:", all_sizes[0] * all_sizes[1] * all_sizes[2])

