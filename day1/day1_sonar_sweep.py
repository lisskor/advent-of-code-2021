import sys


def read_input(filename):
    with open(filename, 'r', encoding='utf8') as fh:
        lines = [line.strip() for line in fh]
    return [int(line) for line in lines]


def count_increasing_measurements(filename):
    measurements = read_input(filename)
    increased_measurements = sum([1 if measurements[i] > measurements[i-1]
                                  else 0
                                  for i in range(1, len(measurements))])
    return increased_measurements


def count_increasing_windows(filename):
    measurements = read_input(filename)
    increased_measurements = sum([1 if (measurements[i] +
                                        measurements[i-1] +
                                        measurements[i-2]) >
                                       (measurements[i-1] +
                                        measurements[i-2] +
                                        measurements[i-3])
                                  else 0
                                  for i in range(2, len(measurements))])
    return increased_measurements


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    if part == "1":
        print(count_increasing_measurements(input_file))
    elif part == "2":
        print(count_increasing_windows(input_file))



