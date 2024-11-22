import math
import time


class Node:
    """
        Node represents a single point in the A* pathfinding algorithm.

        Attributes
        ----------
        position : tuple
            The coordinates of the node in the grid.
        g : float, optional
            The cost from the start node to this node (default is 0).
        h : float, optional
            The heuristic cost estimate to the goal node (default is 0).
        f : float
            The total cost (f = g + h).
        parent : Node, optional
            The parent node leading to this node (default is None).

        Methods
        -------
        __init__(position, g=0, h=0, parent=None)
            Initializes a new instance of the Node class.
        __eq__(other)
            Checks if this node is equal to another node based on position.
    """
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
    """
    class AStar:

    def __init__(self, grid, start_pos, target_pos, diagonal=False):
        """
    def __init__(self, grid, start_pos, target_pos, diagonal=False, diagonal_cost=True):
        self.grid = grid
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.open_list = []
        self.closed_list = []
        self.path = []
        self.moves = MOVES if diagonal else MOVES[:4]
        self.explored_paths = []
        self.diagonal = diagonal
        self.diagonal_cost = diagonal_cost

    def get_manhattan_distance(self, position, target_position):
        """
        :param position: A tuple containing the x and y coordinates of the current position.
        :param target_position: A tuple containing the x and y coordinates of the target position.
        :return: The Manhattan distance between the current position and the target position.
        """
        return abs(position[0] - target_position[0]) + abs(position[1] - target_position[1])

    def get_euclidean_distance(self, position, target_position):
        """
        :param position: A tuple representing the x and y coordinates of the first point.
        :param target_position: A tuple representing the x and y coordinates of the second point.
        :return: The Euclidean distance between the two points.
        """
        return math.sqrt((position[0] - target_position[0]) ** 2 + (position[1] - target_position[1]) ** 2)


    def add_neighbors(self, init_node):
        """
        :param init_node: The initial node from which neighboring nodes are to be generated.
        :return: None
        """
        for move in self.moves:
            added_g_cost = 1
            if self.diagonal and self.diagonal_cost:
                if move[0] != 0 and move[1] != 0:
                    added_g_cost = math.sqrt(2)
            new_pos = (init_node.position[0] + move[0], init_node.position[1] + move[1])

            # Ensure new position is within grid bounds
            if 0 <= new_pos[0] < len(self.grid) and 0 <= new_pos[1] < len(self.grid[0]):
                if self.grid[new_pos[0]][new_pos[1]] == 0:  # Check if not an obstacle
                    g_cost = init_node.g + added_g_cost
                    h_cost = self.get_euclidean_distance(new_pos, self.target_pos) if self.diagonal else self.get_manhattan_distance(new_pos, self.target_pos)
                    new_node = Node(new_pos, g=g_cost, h=h_cost, parent=init_node)

                    # if node is not already scanned
                    if new_node not in self.closed_list:
                        # get the existing version of the node, if it already exists in the open list
                        existing_node = next((n for n in self.open_list if n == new_node), None)

                        # if the node doesn't already exist, or there is a shorter path to the node, update it
                        if existing_node is None or new_node.f < existing_node.f:
                            if existing_node:
                                self.open_list.remove(existing_node)  # Remove the older version
                            self.open_list.append(new_node)  # Add the updated version

    def find_path(self):
        """
        Finds the shortest path from the start position to the target position using the A* algorithm.

        The method initializes the open list with the start node, and then iteratively processes nodes from the open list
        with the lowest f-score (sum of g-score and h-score). For each processed node, it checks whether the node's position
        matches the target position. If so, it reconstructs the path from the start position to the target position by
        tracing back through the parent nodes and returns the path along with the elapsed time.

        :return: A tuple containing the list of positions representing the path from the start position to the target position,
            and the time taken to find the path.
        """
        start_time = time.time()
        start_node = Node(self.start_pos, h=self.get_manhattan_distance(self.start_pos, self.target_pos))
        self.open_list.append(start_node)

        self.path = []

        while self.open_list:
            # curr node is set to the smallest f value
            curr_node = min(self.open_list, key=lambda node: node.f)

            # removes the curr node from open list and adds it to closed list
            self.open_list.remove(curr_node)
            self.closed_list.append(curr_node)

            # if the curr_node is the target
            if curr_node.position == self.target_pos:
                total_cost = curr_node.g
                while curr_node.parent:
                    self.path.append(curr_node.position)
                    curr_node = curr_node.parent
                self.path.append(self.start_pos)
                self.path.reverse()
                end_time = time.time()
                return self.path, (end_time - start_time), total_cost

            self.add_neighbors(curr_node)

            if not self.open_list:
                return None, (time.time() - start_time)

    def get_explored_paths(self):
        """
        :return: The list of lists where each inner list contains the positions retraced from the start node to the current node.
        """
        self.explored_paths = []
        for curr_node in self.closed_list:
            retraced_path = []
            while curr_node.parent:
                retraced_path.append(curr_node.position)
                curr_node = curr_node.parent
            self.explored_paths.append(retraced_path)
        return self.explored_paths
