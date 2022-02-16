import sys


def read_input(filename: str):
    with open(filename, 'r', encoding='utf8') as fh:
        lines = [line.strip() for line in fh]
    return lines


def most_common_bit(input_bits: list):
    bits_sum = sum([int(bit) for bit in input_bits])
    if bits_sum > len(input_bits) - bits_sum:
        return "1"
    elif bits_sum < len(input_bits) - bits_sum:
        return "0"
    else:
        return None


def calculate_gamma_epsilon(input_lines: list[str]):
    line_length = len(input_lines[0])
    most_common_bits, least_common_bits = "", ""
    for i in range(line_length):
        most_common_bits += most_common_bit([line[i] for line in input_lines])
    least_common_bits = ''.join(["0" if mcb == "1" else "1" for mcb in most_common_bits])
    return most_common_bits, least_common_bits


def generator_rating(input_lines: list[str], co2: bool = False):
    line_length = len(input_lines[0])
    remaining_lines = input_lines
    for i in range(line_length):
        mcb = most_common_bit([line[i] for line in remaining_lines])
        if not co2:
            if mcb:
                remaining_lines = [line for line in remaining_lines if line[i] == mcb]
            else:
                remaining_lines = [line for line in remaining_lines if line[i] == "1"]
        else:
            if mcb:
                remaining_lines = [line for line in remaining_lines if line[i] != mcb]
            else:
                remaining_lines = [line for line in remaining_lines if line[i] == "0"]
        # print(i, remaining_lines)
        if len(remaining_lines) == 1:
            break
    return remaining_lines[0]


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
        if part == "1":
            gamma, epsilon = calculate_gamma_epsilon(read_input(input_file))
            print(gamma, epsilon)
            print(int(gamma, 2) * int(epsilon, 2))
        elif part == "2":
            oxygen_gen_rating = generator_rating(read_input(input_file), co2=False)
            co2_scrub_rating = generator_rating(read_input(input_file), co2=True)
            print("Oxygen generator:", oxygen_gen_rating)
            print("CO2 scrubber:", co2_scrub_rating)
            print(int(oxygen_gen_rating, 2) * int(co2_scrub_rating, 2))
    except IndexError:
        print("Specify the task part")

