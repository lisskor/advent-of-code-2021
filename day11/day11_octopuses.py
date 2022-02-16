import sys
import numpy as np


def read_input(filename: str):
    with open(filename, 'r', encoding='utf8') as fh:
        lines = [[int(ch) for ch in line.strip()] for line in fh]
    return np.array(lines, dtype=int)


def neighbor_indices(x: int, y: int):
    indices = [(x - 1, y), (x + 1, y),
               (x, y - 1), (x, y + 1),
               (x - 1, y - 1), (x - 1, y + 1),
               (x + 1, y - 1), (x + 1, y + 1)]
    return indices


class OctopusGrid:
    def __init__(self, energy: np.array):
        self.energy = energy
        self.rows, self.columns = 10, 10
        self.padded_grid = np.zeros((self.rows+2, self.columns+2))
        # fill edges with -1
        self.padded_grid[0, :] = -1
        self.padded_grid[:, 0] = -1
        self.padded_grid[-1, :] = -1
        self.padded_grid[:, -1] = -1

        self.total_flashes = 0

    def __repr__(self):
        out_string = str(self.energy)
        return out_string

    def adjacent_nodes(self, x: int, y: int):
        return [n for n in neighbor_indices(x, y)
                if self.padded_grid[n[0]+1, n[1]+1] != -1]

    def time_steps(self, num_steps: int):
        for step in range(num_steps):
            self.energy += 1
            while np.any(self.energy > 9):
                flashers = np.argwhere(self.energy > 9)
                self.energy[self.energy > 9] = 0
                for flasher in flashers:
                    self.total_flashes += 1
                    neighbors = [n for n in self.adjacent_nodes(flasher[0], flasher[1])
                                 if self.energy[n[0], n[1]] != 0]
                    for neighbor in neighbors:
                        self.energy[neighbor] += 1

    def find_first_sync_flash(self):
        current_time = 0
        while True:
            current_time += 1
            self.time_steps(1)
            if np.count_nonzero(self.energy) == 0:
                break
        return current_time


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
        steps = int(sys.argv[3])
    except IndexError:
        print("Specify the task part and number of steps")
        exit(1)

    octopus_grid = OctopusGrid(read_input(input_file))
    if part == "1":
        octopus_grid.time_steps(steps)
        print('Final grid:\n', octopus_grid.energy)
        print('Total flashes:', octopus_grid.total_flashes)
    elif part == "2":
        first_sync_flash = octopus_grid.find_first_sync_flash()
        print('All octopuses flashed at step', first_sync_flash)

