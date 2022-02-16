import sys
import numpy as np


def read_input(filename: str):
    with open(filename, 'r', encoding='utf8') as fh:
        lines = [line.strip() for line in fh]
    numbers_called = np.array([int(num) for num in lines[0].split(',')], dtype=int)
    boards = np.zeros((len(lines)//6, 5, 5), dtype=int)

    board_counter, line_counter = 0, 0
    for i, line in enumerate(lines[2:]):
        if not line:
            board_counter += 1
            line_counter = 0
        else:
            boards[board_counter, line_counter] = [int(el) for el in line.split()]
            line_counter += 1

    return numbers_called, boards


class BingoBoard:
    def __init__(self, numbers: np.array):
        self.board = numbers
        self.marked = np.zeros_like(self.board)
        self.won = False

    def __repr__(self):
        out_string = ""
        columns_marked = self.marked.sum(0) > 0
        column_widths = [4 if columns_marked[i] else 2 for i in range(5)]
        for line_num in range(5):
            for col_num in range(5):
                num = str(self.board[line_num, col_num])
                if not self.marked[line_num, col_num]:
                    out_string += ' ' * (column_widths[col_num] - len(num)) + num + ' '
                else:
                    out_string += ' ' * (column_widths[col_num] - len(num) - 2) + '*' + num + '*' + ' '
            out_string += '\n'
        return out_string

    def mark_number(self, number: int):
        # mark the number
        self.marked[self.board == number] = 1

        # check if the board has won
        if np.any(self.marked.sum(0) == 5) or np.any(self.marked.sum(1) == 5):
            self.won = True

    def calculate_score(self, last_called: int):
        unmarked_sum = self.board[self.marked == 0].sum()
        return int(unmarked_sum * last_called)


class BingoBoardSet(list):
    def __init__(self, boards: list[BingoBoard]):
        super(BingoBoardSet, self).__init__(boards)
        self.boards = boards
        self.won = np.array([b.won for b in self.boards])
        self.last_number_called = None

    def mark_number_on_set(self, number):
        for board in self.boards:
            board.mark_number(number)
        self.won = np.array([b.won for b in self.boards])
        self.last_number_called = number


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    input_called_numbers, input_board_numbers = read_input(input_file)
    input_boards = BingoBoardSet([BingoBoard(bn) for bn in input_board_numbers])
    if part == "1":
        for n in input_called_numbers:
            input_boards.mark_number_on_set(n)
            if np.any(input_boards.won):
                winning_board = np.where(input_boards.won)[0][0]
                winning_score = input_boards[winning_board].calculate_score(input_boards.last_number_called)
                print(f"Board number {winning_board} won, the score is {winning_score}")
                print("\nWinning board:")
                print(input_boards[winning_board])
                break

    elif part == "2":
        last_board = None
        for n in input_called_numbers:
            input_boards.mark_number_on_set(n)
            boards_not_won = np.where(input_boards.won, 0, 1)
            if boards_not_won.sum() == 1:
                last_board = np.where(boards_not_won)[0][0]
            elif boards_not_won.sum() == 0:
                last_winning_score = input_boards[last_board].calculate_score(input_boards.last_number_called)
                print(f"Board number {last_board} won last, the score is {last_winning_score}")
                print("\nLast winning board:")
                print(input_boards[last_board])
                break
