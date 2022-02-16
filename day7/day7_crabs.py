import sys
import numpy as np


def read_input(filename: str):
    with open(filename, 'r', encoding='utf8') as fh:
        pos_list = [int(n) for n in fh.readline().split(',')]
    return pos_list


def brute_force_constant(crab_positions: list[int]):
    max_position = max(crab_positions)
    total_fuel = {pos: sum([abs(current - pos)
                            for current in crab_positions])
                  for pos in range(max_position)}
    best_position = min(total_fuel, key=total_fuel.get)
    best_fuel = total_fuel[best_position]
    return best_position, best_fuel


def progressive_fuel(steps: int):
    return (steps * (steps + 1)) // 2


def brute_force_changing(crab_positions: list[int]):
    max_position = max(crab_positions)
    total_fuel = {pos: sum([progressive_fuel(abs(current - pos))
                            for current in crab_positions])
                  for pos in range(max_position)}
    best_position = min(total_fuel, key=total_fuel.get)
    best_fuel = total_fuel[best_position]
    return best_position, best_fuel


def fuel_to_mean(crab_positions: list[int]):
    mean_position = round(np.mean(crab_positions))
    fuel_needed = sum([progressive_fuel(abs(current - mean_position))
                       for current in crab_positions])
    return mean_position, fuel_needed


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    if part == "1":
        position, fuel = brute_force_constant(read_input(input_file))
        print(f"Best position: {position}, fuel: {fuel}")
    elif part == "2":
        position, fuel = brute_force_changing(read_input(input_file))
        print(f"Best position: {position}, fuel: {fuel}")
