class Node:
    def __init__(self, position, g=0, h=0, parent=None):
        self.position = position
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __eq__(self, other):
        return self.position == other.position

# Define possible moves: up, down, left, right
MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]

class AStar:
    def __init__(self, grid, start_pos, target_pos, diagonal=False):
        self.grid = grid
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.open_list = []
        self.closed_list = []
        self.path = []
        self.moves = MOVES if diagonal else MOVES[:4]

    def get_manhattan_distance(self, position, target_position):
        return abs(position[0] - target_position[0]) + abs(position[1] - target_position[1])


    def add_neighbors(self, init_node):
        for move in self.moves:
            new_pos = (init_node.position[0] + move[0], init_node.position[1] + move[1])

            # Ensure new position is within grid bounds
            if 0 <= new_pos[0] < len(self.grid) and 0 <= new_pos[1] < len(self.grid[0]):
                if self.grid[new_pos[0]][new_pos[1]] == 0:  # Check if walkable
                    g_cost = init_node.g + 1  # Assuming each move costs 1
                    h_cost = self.get_manhattan_distance(new_pos, self.target_pos)
                    new_node = Node(new_pos, g=g_cost, h=h_cost, parent=init_node)

                    # Check if this node is in the open list or needs to be updated
                    if new_node not in self.open_list or new_node.f < next((n for n in self.open_list if n == new_node), new_node).f:
                        self.open_list.append(new_node)

    def find_path(self):
        start_node = Node(self.start_pos, h=self.get_manhattan_distance(self.start_pos, self.target_pos))
        self.open_list.append(start_node)

        while self.open_list:
            curr_node = min(self.open_list, key=lambda node: node.f)

            self.open_list.remove(curr_node)
            self.closed_list.append(curr_node)

            if curr_node.position == self.target_pos:
                while curr_node.parent:
                    self.path.append(curr_node.position)
                    curr_node = curr_node.parent
                self.path.append(self.start_pos)
                self.path.reverse()
                return self.path

            self.add_neighbors(curr_node)
