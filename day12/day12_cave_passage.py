import sys
from collections import Counter


def read_input(filename: str):
    with open(filename, 'r', encoding='utf8') as fh:
        lines = [line.strip().split('-') for line in fh]
    return lines


class CaveGraph:
    def __init__(self, edges: list):
        self.nodes = {}
        for edge in edges:
            self.nodes.setdefault(edge[0], set())
            self.nodes.setdefault(edge[1], set())
            self.nodes[edge[0]].add(edge[1])
            self.nodes[edge[1]].add(edge[0])

        self.big = {node: True if node.isupper() else False for node in self.nodes}
        self.valid_paths = []
        self.valid_paths_with_one_repeat = []

    def dfs(self, start: str = 'start', backtrack: list[str] = []):
        for point in self.nodes[start]:
            if point in backtrack and not self.big[point]:
                pass
            elif point == 'end':
                self.valid_paths.append(backtrack + [start, point])
            else:
                self.dfs(point, backtrack + [start])

    def allowed_to_add(self, node: str, backtrack: list[str]):
        backtrack_counter = Counter(backtrack)
        # check if any small node has been visited twice
        more_small_repeats_allowed = True
        for n in backtrack_counter:
            if backtrack_counter[n] > 1 and not self.big[n]:
                more_small_repeats_allowed = False
                break

        if self.big[node]:
            return True
        elif node == 'start' or node == 'end':
            return False
        elif not self.big[node]:
            if more_small_repeats_allowed:
                return True
            else:
                if node in backtrack:
                    return False
                else:
                    return True

    def dfs_with_one_repeat(self, start: str = 'start', backtrack: list[str] = []):
        for point in self.nodes[start]:
            if point == 'end':
                self.valid_paths_with_one_repeat.append(backtrack + [start, point])
            elif not self.allowed_to_add(point, backtrack + [start]):
                pass
            else:
                self.dfs_with_one_repeat(point, backtrack + [start])


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    input_text = read_input(input_file)
    cave_graph = CaveGraph(input_text)
    if part == "1":
        cave_graph.dfs()
        # for path in sorted(cave_graph.valid_paths):
        #     print(path)
        print(f"There are {len(cave_graph.valid_paths)} valid paths")
    elif part == "2":
        cave_graph.dfs_with_one_repeat()
        # for path in sorted(cave_graph.valid_paths_with_one_repeat):
        #     print(path)
        print(f"There are {len(cave_graph.valid_paths_with_one_repeat)} valid paths")

