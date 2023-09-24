# Amphipods should never rest in front of an entrance.
# Amphipods have 3 states: Standby, Move, and Rest (0, 1, 2)
# Two methods of movement: 0->1, 1->2

#           1
# 01234567890
 #############
 #...........#  0
 ###B#C#B#D###  1
   #A#D#C#A#    2
   #########

# Possible moves: 00, 01, 03, 05, 07, 09, 0 10

import heapq
import itertools

MAX = 1e7
energy_table = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}


def hash_dict(dictionary):
    return tuple(sorted(dictionary.items()))


def reverse_hash_dict(hash):
    return dict(hash)


class PriorityQueue:

    REMOVED = "REMOVED"

    def __init__(self):
        self.queue = []
        self.table = {}
        self.removed = set()
        self.counter = itertools.count()

    def insert(self, item, priority):
        if item in self.table:
            self.remove(item)
        count_id = next(self.counter)
        entry = [priority, count_id, item]
        self.table[item] = entry
        heapq.heappush(self.queue, entry)

    def remove(self, item):
        entry = self.table.pop(item)
        entry[-1] = PriorityQueue.REMOVED

    def pop(self):
        while self.queue:
            priority, count, task = heapq.heappop(self.queue)
            if task is not PriorityQueue.REMOVED:
                del self.table[task]
                return task
        raise KeyError('pop from an empty priority queue')


scores = {}


# Heuristic function
def h(state):
    key = hash_dict(state)
    if key in scores:
        return scores[key]

    # Optimal energy = Sum(1~n) + Moving out + move to shaft
    energy = 0
    count = {"A": 0, "B": 0, "C": 0, "D": 0}
    for location, info in state.items():
        r, c = location
        ltr, mode = info
        if ltr in count and mode != 2:
            count[ltr] += 1
            correct_col = (ord(ltr) - 64) * 2
            steps = r + abs(c - correct_col) + count[ltr]
            energy += energy_table[ltr] * steps

    scores[key] = energy
    return energy


def main(file, log_all=False):

    # Read the grid
    with open(file) as f:
        grid = list(map(lambda x: list(x.strip().replace("#", "")), f.readlines()))[2:-1]

    # Number of amphipods per type
    amphipods_count = len(grid)

    # Generate state of the map
    cells = [0, 1, 3, 5, 7, 9, 10]
    in_valid_position = [True] * 4
    start_state = dict([((0, location), (None, None)) for location in cells])
    end_state = dict([((0, location), (None, None)) for location in cells])

    # We iterate using reverse order
    for i, row in enumerate(grid[::-1]):
        for j in range(len(row)):
            creature = row[j]
            coordinate = amphipods_count - i, (j+1)*2
            if "ABCD"[j] == creature and in_valid_position[j]:
                # The creature is already sorted
                start_state[coordinate] = (creature, 2)
            else:
                start_state[coordinate] = (creature, 0)
                in_valid_position[j] = False

            end_state[coordinate] = (chr(65 + j), 2)

    # Run A*

    starting_node = hash_dict(start_state)
    distances = {starting_node: 0}
    parent = {starting_node: None}

    visited = set()

    queue = PriorityQueue()
    queue.insert(starting_node, priority=0)

    def visualize(dictionary):
        txt = ""
        for r in range(-1, amphipods_count+2):
            for c in range(0, 11):
                if (r, c) in dictionary:
                    ltr = dictionary[(r, c)][0]
                    if ltr is None:
                        txt += "."
                    else:
                        txt += ltr
                elif r == 0:
                    txt += "."
                else:
                    txt += "#"
            txt += "\n"
        txt += "\n"
        return txt

    while True:
        try:
            # Vertex v = node in queue minimizing distance (Energy)
            node = queue.pop()
            state = reverse_hash_dict(node)
            # print(visualize(state))
        except KeyError:
            print("Oh no")
            break

        visited.add(node)

        if all([state[key][0] == end_state[key][0] for key in end_state]):
            print("Answer:", distances[hash_dict(end_state)])
            print("Nodes visited:", len(visited))
            # with open("path.txt", "w") as f:
            #     next = hash_dict(end_state)
            #     while next is not None:
            #         f.write(visualize(reverse_hash_dict(next)))
            #         f.write("Energy: " + str(distances[next]) + "\n\n")
            #         next = parent[next]
            break

        # for neighbours of node, add neighbours inside queue and compute their distance
        for location, info in state.items():

            row, col = location
            creature, mode = info
            if creature is None or mode == 2:
                continue

            accessible_spaces = []

            if mode == 1:
                correct_col = (ord(creature) - 64) * 2

                # Check if there is a path to the shaft
                accessible = True
                if col > correct_col:
                    for c in range(col-1, correct_col, -1):
                        if c in cells and state[(0, c)][0] is not None:
                            accessible = False
                            break
                elif col < correct_col:
                    for c in range(col+1, correct_col):
                        if c in cells and state[(0, c)][0] is not None:
                            accessible = False
                            break

                if not accessible:
                    continue

                # Check if the shaft is empty or have spaces
                furthest = amphipods_count
                for r in range(amphipods_count, 0, -1):
                    if state[(r, correct_col)][0] not in [None, creature]:
                        break
                    if state[(r, correct_col)][0] is creature:
                        furthest = r - 1
                else:
                    if furthest >= 1:
                        steps = abs(furthest - row) + abs(correct_col - col)
                        accessible_spaces += [(furthest, correct_col, steps, 2)]

            if mode == 0:
                # Check if it can exit the hallway
                # e.g. if row = 3, then check 1 and 2
                for r in range(1, row):
                    if state[(r, col)][0] is not None:
                        break
                else:
                    # Check accessibility to hallway spaces
                    # cells = [0, 1, 3, 5, 7, 9, 10]
                    accessible_cols = []

                    for generator in [range(col-1, cells[0]-1, -1), range(col+1, cells[-1]+1)]:
                        for c in generator:
                            if c in cells:
                                if state[(0, c)][0] is None:
                                    accessible_cols.append(c)
                                else:
                                    break

                    # Can move amphipods to (0, accessible_cols), create new node
                    for c in accessible_cols:
                        steps = abs(row) + abs(c - col)
                        accessible_spaces += [(0, c, steps, 1)]

            for space in accessible_spaces:
                nr, nc, n_steps, n_mode = space
                new_state = state.copy()
                new_state[(row, col)] = (None, None)
                new_state[(nr, nc)] = (creature, n_mode)

                # Generate new node
                new_node = hash_dict(new_state)
                if new_node not in visited:
                    new_distance = distances[node] + n_steps * energy_table[creature]
                    score = new_distance + h(new_state)
                    if new_node in distances:
                        if distances[new_node] > new_distance:
                            queue.insert(new_node, score)
                            distances[new_node] = new_distance
                            parent[new_node] = node
                    else:
                        queue.insert(new_node, score)
                        distances[new_node] = new_distance
                        parent[new_node] = node
