import sys


class SubmarinePosition:
    def __init__(self):
        self.horizontal = 0
        self.depth = 0

    def __repr__(self):
        return f"SubmarinePosition: horizontal {self.horizontal}, depth {self.depth}"

    def increase_horizontal(self, value: int):
        self.horizontal += value

    def increase_depth(self, value: int):
        self.depth += value

    def decrease_depth(self, value: int):
        self.depth -= value


class SubmarinePositionWithAim:
    def __init__(self):
        self.aim = 0
        self.horizontal = 0
        self.depth = 0

    def __repr__(self):
        return f"SubmarinePosition: aim {self.aim}, horizontal {self.horizontal}, depth {self.depth}"

    def down(self, value: int):
        self.aim += value

    def up(self, value: int):
        self.aim -= value

    def forward(self, value: int):
        self.horizontal += value
        self.depth += self.aim * value


def process_input(position: SubmarinePosition, filename: str):
    with open(filename, 'r', encoding='utf8') as fh:
        lines = [line.strip().split() for line in fh]
    for command, num in lines:
        v = int(num)
        if command == "forward":
            position.increase_horizontal(v)
        elif command == "down":
            position.increase_depth(v)
        elif command == "up":
            position.decrease_depth(v)
    return position


def process_input_with_aim(position: SubmarinePositionWithAim, filename: str):
    with open(filename, 'r', encoding='utf8') as fh:
        lines = [line.strip().split() for line in fh]
    for command, num in lines:
        v = int(num)
        if command == "forward":
            position.forward(v)
        elif command == "down":
            position.down(v)
        elif command == "up":
            position.up(v)
    return position


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    if part == "1":
        my_position = SubmarinePosition()
        process_input(my_position, input_file)
        print(my_position)
        print(my_position.horizontal * my_position.depth)
    elif part == "2":
        my_position = SubmarinePositionWithAim()
        process_input_with_aim(my_position, input_file)
        print(my_position)
        print(my_position.horizontal * my_position.depth)
