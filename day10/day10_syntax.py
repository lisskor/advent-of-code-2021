import sys


def read_input(filename: str):
    with open(filename, 'r', encoding='utf8') as fh:
        lines = [line.strip() for line in fh]
    return lines


def is_corrupted(line: str):
    costs = {')': 3, ']': 57, '}': 1197, '>': 25137}
    opening_chars = '(<[{'
    closing_chars = ')>]}'
    close_open = {')': '(', '>': '<', ']': '[', '}': '{'}
    open_chunks = []
    for char in line:
        if char in opening_chars:
            open_chunks.append(char)
        if char in closing_chars:
            if open_chunks.pop() != close_open[char]:
                return costs[char]
    return 0


def completion_score(line: str):
    costs = {'(': 1, '[': 2, '{': 3, '<': 4}
    opening_chars = '(<[{'
    closing_chars = ')>]}'
    open_close = {'(': ')', '<': '>', '[': ']', '{': '}'}
    open_chunks = []
    completing_chars = ""
    total_score = 0
    for char in line:
        if char in opening_chars:
            open_chunks.append(char)
        elif char in closing_chars:
            open_chunks.pop()
    for char in open_chunks[::-1]:
        completing_chars += open_close[char]
        total_score = total_score * 5 + costs[char]
    return total_score


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    inp_lines = read_input(input_file)
    if part == "1":
        total_cost = 0
        for inp_line in inp_lines:
            total_cost += is_corrupted(inp_line)
        print(total_cost)
    elif part == "2":
        scores = []
        for inp_line in inp_lines:
            if is_corrupted(inp_line) > 0:
                continue
            else:
                scores.append(completion_score(inp_line))
        middle_score = sorted(scores)[len(scores)//2]
        print("Middle score:", middle_score)
