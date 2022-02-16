import sys
from collections import Counter


def read_input(filename: str):
    with open(filename, 'r', encoding='utf8') as fh:
        timers_list = [int(n) for n in fh.readline().split(',')]
    return timers_list


class LanternFish:
    def __init__(self, timer: int):
        self.timer = timer
        self.spawn = False

    def __repr__(self):
        return str(self.timer)

    def time_step(self):
        if self.timer > 0:
            self.spawn = False
            self.timer -= 1
        elif self.timer == 0:
            self.spawn = True
            self.timer = 6


class LanternFishSchool:
    def __init__(self, timers: list[int]):
        self.members = [LanternFish(t) for t in timers]

    def time_step(self):
        for member in self.members:
            member.time_step()
        new_spawn = sum([member.spawn for member in self.members])
        for i in range(new_spawn):
            self.members.append(LanternFish(8))


class LanternFishSchoolDict:
    def __init__(self, timers: list[int]):
        self.members_by_timer = {i: Counter(timers)[i] for i in range(9)}

    def time_step(self):
        new_spawn = self.members_by_timer[0]
        for i in range(8):
            self.members_by_timer[i] = self.members_by_timer[i+1]
        self.members_by_timer[6] += new_spawn
        self.members_by_timer[8] = new_spawn

    def size(self):
        return sum([self.members_by_timer[t] for t in self.members_by_timer])


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        days = int(sys.argv[2])
        part = sys.argv[3]
    except IndexError:
        print("Task part or number of days not specified")
        exit(1)

    input_ages = read_input(input_file)
    if part == "1":
        school = LanternFishSchool(input_ages)
        for day in range(days):
            school.time_step()
        print(f"After {days} days there are {len(school.members)} fish")
    elif part == "2":
        school = LanternFishSchoolDict(input_ages)
        for day in range(days):
            school.time_step()
        print(f"After {days} days there are {school.size()} fish")
