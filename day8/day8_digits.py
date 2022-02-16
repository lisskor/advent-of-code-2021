import sys
from collections import Counter


def read_input(filename: str):
    with open(filename, 'r', encoding='utf8') as fh:
        lines = [[el.split() for el in line.strip().split(' | ')] for line in fh]
    return lines


def count_simple_digits(observations: list[list[list[str]]]):
    simple_digits_counter = 0
    for observation in observations:
        output_digits = observation[1]
        simple_digits_counter += len([len(d)
                                      for d in output_digits
                                      if len(d) in [2, 3, 4, 7]])
    return simple_digits_counter


def reconstruct_digits(observation: list[list[str]]):
    digit_segments = {0: 'abcefg', 1: 'cf', 2: 'acdeg',
                      3: 'acdfg', 4: 'bcdf', 5: 'abdfg',
                      6: 'abdefg', 7: 'acf', 8: 'abcdefg',
                      9: 'abcdfg'}
    num_segments = {i: len(digit_segments[i]) for i in digit_segments}
    broken_mapping = {char: 'abcdefg' for char in 'abcdefg'}
    unique_observations = observation[0]
    unique_observations_mapping = {i: None for i in range(10)}
    segment_occurences = {'a': 8, 'b': 6, 'c': 8,
                          'd': 7, 'e': 4, 'f': 9,
                          'g': 7}
    simple_digits = [1, 7, 4, 8]
    complex_digits = [0, 2, 3, 5, 6, 9]

    # first, segments for unambiguous digits
    unique_observations_mapping[1] = [d for d in unique_observations if len(d) == 2][0]
    unique_observations_mapping[7] = [d for d in unique_observations if len(d) == 3][0]
    unique_observations_mapping[4] = [d for d in unique_observations if len(d) == 4][0]
    unique_observations_mapping[8] = [d for d in unique_observations if len(d) == 7][0]

    segment_counter = Counter("".join(unique_observations))
    # segment appears 6 times -> B
    broken_mapping['b'] = [item[0] for item in segment_counter.items() if item[1] == 6][0]
    # segment appears 4 times -> E
    broken_mapping['e'] = [item[0] for item in segment_counter.items() if item[1] == 4][0]
    # segment appears 9 times -> F
    broken_mapping['f'] = [item[0] for item in segment_counter.items() if item[1] == 9][0]

    # if a segment is in 7, but not 1, it is A
    broken_mapping['a'] = list(
        set(
            unique_observations_mapping[7]
        ).difference(
            set(unique_observations_mapping[1])
        )
    )[0]
    # C is in 1 and 7, and not F
    broken_mapping['c'] = list(
        set(unique_observations_mapping[7]
            ).intersection(
            set(unique_observations_mapping[1]
                )
        ).difference(
            set(broken_mapping['f'])
        ))[0]

    # remove unambiguously found segments from candidates
    for s in ['a', 'b', 'c', 'e', 'f']:
        for k in ['d', 'g']:
            broken_mapping[k] = broken_mapping[k].replace(broken_mapping[s], '')

    # distinguish between D and G: in simple digits, G appears only once
    simple_digits_segment_counter = Counter("".join(
        ["".join(unique_observations_mapping[d]) for d in simple_digits]
    ))
    for segment in broken_mapping['d']:
        if simple_digits_segment_counter[segment] == 1:
            broken_mapping['g'] = segment
            break
    broken_mapping['d'] = broken_mapping['d'].replace(broken_mapping['g'], '')

    # segments for ambiguous digits
    for d in complex_digits:
        unique_observations_mapping[d] = "".join([broken_mapping[ch] for ch in digit_segments[d]])

    # sort strings alphabetically
    for d in unique_observations_mapping:
        unique_observations_mapping[d] = "".join(sorted(unique_observations_mapping[d]))

    return unique_observations_mapping, broken_mapping


def decipher_output_digits(output_digits: list[str], digit_mapping: dict):
    deciphered_digits = []
    segments_to_digits = {digit_mapping[k]: k for k in digit_mapping}
    for d in output_digits:
        deciphered_digits.append(segments_to_digits["".join(sorted(d))])
    return int("".join([str(i) for i in deciphered_digits]))


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    input_observations = read_input(input_file)
    if part == "1":
        print(count_simple_digits(input_observations))
    elif part == "2":
        output_numbers = []
        for inp in input_observations:
            digits, segments = reconstruct_digits(inp)
            output_numbers.append(decipher_output_digits(inp[1], digits))
        print("Sum of deciphered output numbers:", sum(output_numbers))
