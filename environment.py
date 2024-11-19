import time

import pygame
from pygame import gfxdraw
import sys

from alg import AStar

# Set up screen dimensions
dimensions = (20, 20)
block_size = 30
width, height = dimensions[0] * block_size, dimensions[1] * block_size

# Set up display
screen = pygame.display.set_mode((width + 10, height + 40))
pygame.display.set_caption('A* Board')

# Define colors
BACKGROUND_COLOR = (247, 247, 247)
LIGHT_GRAY = (180, 180, 180)

START_CONST_COLOR = (255, 0, 0)
TARGET_CONST_COLOR = (0, 255, 0)
OBSTACLE_CONST_COLOR = (0, 0, 0)
SELECTED_OUTLINE_COLOR = (0, 0, 255)

class Environment:
    """
    ====================================
    Environment Class
    ====================================

    class Environment:
        Manages the pathfinding environment with grid, start and target positions, obstacles, and visualization.

        Parameters:
        -----------
        start_pos : tuple
            Coordinates for the starting position on the grid.
        target_pos : tuple
            Coordinates for the target position on the grid.
        diagonal : bool, optional
            Indicates if diagonal movement is allowed (default is False).
        highlight_explored_path : bool, optional
            Indicates if the explored path should be highlighted during visualization (default is False).

        Attributes:
        -----------
        start : tuple
            Current starting position on the grid.
        target : tuple
            Current target position on the grid.
        grid : list
            2D list representing the grid.
        current_placement_piece : int
            Indicates the current piece being placed (0 for start, 1 for target, 2 for obstacle).
        obstacles : list
            List of obstacle coordinates.
        path : list
            List of coordinates representing the found path.
        time : float
            Time taken to find the path.
        diagonal : bool
            Indicates if diagonal movement is allowed.
        highlight_explored_path : bool
            Indicates if the explored path should be highlighted.
        explored_path : list
            List of explored paths during pathfinding.
        start_circle_outline_color : tuple
            RGB color for the start circle outline.
        target_circle_outline_color : tuple
            RGB color for the target circle outline.
        obstacle_outline_color : tuple
            RGB color for the obstacle outline.

        Methods:
        --------
        update_path():
            Calculates the path using A* algorithm and updates the path and explored path.
        update_obstacles(grid):
            Updates the list of obstacles based on the current grid.
        run_env():
            Runs the environment visualization, including handling user interactions and updating the display.
    """
    def __init__(self, start_pos, target_pos, diagonal=False, highlight_explored_path=False):
        self.start = start_pos
        self.target = target_pos
        self.grid = [[0 for _ in range(dimensions[0])] for _ in range(dimensions[1])]
        # 0 -> Start, 1 -> End, 2 -> Obstacle
        self.current_placement_piece = 0
        self.obstacles = []
        self.path = []
        self.time = 0

        self.diagonal = diagonal

        self.highlight_explored_path = highlight_explored_path
        self.explored_path = []

    def update_path(self):
        """
        Updates the path using the A* algorithm.

        :return: None
        """
        alg = AStar(self.grid, self.start, self.target, self.diagonal)
        self.path, self.time = alg.find_path()
        self.explored_path = alg.get_explored_paths()

    def update_obstacles(self, grid):
        """
        :param grid: 2D list representing the grid where 0 denotes free space and 1 denotes an obstacle
        :return: None
        """
        self.obstacles = []
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == 1:
                    self.obstacles.append((row, col))

    def run_env(self):
        """
        Runs the environment and handles the main game loop using Pygame.

        :return: None
        """
        # Initialize Pygame
        pygame.init()

        font = pygame.font.Font(None, 32)

        # updates path using alg and obstacles
        self.update_path()
        self.update_obstacles(self.grid)

        explored_path_idx = 0

        # Run the game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # on click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        # if user is clicking the grid
                        if pos[1] > 40:
                            col = (pos[0] - 5) // block_size
                            row = (pos[1] - 35) // block_size
                            # depending on placement piece, updates what objects were clicked
                            if self.current_placement_piece == 2:
                                self.grid[row][col] = (1 - self.grid[row][col])
                                self.update_obstacles(self.grid)
                            elif self.current_placement_piece == 0:
                                self.start = (row, col)
                            else:
                                self.target = (row, col)
                            self.update_path()
                            explored_path_idx = 0
                        # if user is clicking menu options
                        else:
                            col = (pos[0]) // block_size

                            # sets placement pieces (start, target, obstacle)
                            if col == 0:
                                self.current_placement_piece = 0
                            elif col == 1:
                                self.current_placement_piece = 1
                            elif col == 2:
                                self.current_placement_piece = 2
                            elif col == 3:
                                self.highlight_explored_path = not self.highlight_explored_path
                                self.update_path()
                                explored_path_idx = 0

            # Fill the background
            screen.fill(BACKGROUND_COLOR)

            # draws menu options
            pygame.gfxdraw.filled_circle(
                screen,
                block_size // 2 + 5,
                40 // 2 - 3,
                block_size // 2 - 9,
                START_CONST_COLOR,
            )
            pygame.gfxdraw.aacircle(
                screen,
                block_size // 2 + 5,
                40 // 2 - 3,
                block_size // 2 - 9,
                SELECTED_OUTLINE_COLOR if self.current_placement_piece == 0 else START_CONST_COLOR,
            )

            pygame.gfxdraw.filled_circle(
                screen,
                block_size + block_size // 2 + 5,
                40 // 2 - 3,
                block_size // 2 - 9,
                TARGET_CONST_COLOR,
            )
            pygame.gfxdraw.aacircle(
                screen,
                block_size + block_size // 2 + 5,
                40 // 2 - 3,
                block_size // 2 - 9,
                SELECTED_OUTLINE_COLOR if self.current_placement_piece == 1 else TARGET_CONST_COLOR,
            )

            pygame.gfxdraw.filled_circle(
                screen,
                block_size * 2 + block_size // 2 + 5,
                40 // 2 - 3,
                block_size // 2 - 9,
                OBSTACLE_CONST_COLOR,
            )
            pygame.gfxdraw.aacircle(
                screen,
                block_size * 2 + block_size // 2 + 5,
                40 // 2 - 3,
                block_size // 2 - 9,
                SELECTED_OUTLINE_COLOR if self.current_placement_piece == 2 else OBSTACLE_CONST_COLOR,
            )

            pygame.gfxdraw.aacircle(
                screen,
                block_size * 3 + block_size // 2 + 5,
                40 // 2 - 3,
                block_size // 2 - 9,
                SELECTED_OUTLINE_COLOR if self.highlight_explored_path else OBSTACLE_CONST_COLOR,
            )

            # Draw the chessboard blocks
            for row in range(dimensions[1]):
                for col in range(dimensions[0]):
                    # draws squares
                    rect = pygame.Rect(col * block_size + 5, row * block_size + 35, block_size, block_size)
                    full_rect = pygame.Rect(5, 35, width, height)
                    # Add an outline to each square
                    pygame.draw.rect(screen, LIGHT_GRAY, full_rect, 2)
                    pygame.draw.rect(screen, LIGHT_GRAY, rect, 1)

                    # draws target, obstacles, path, and start
                    if self.target and self.target == (row, col):
                        pygame.gfxdraw.aacircle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 35,
                            block_size // 2 - 9,
                            (0, 255, 0),
                        )
                        pygame.gfxdraw.filled_circle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 35,
                            block_size // 2 - 9,
                            (0, 255, 0),
                        )
                    elif self.start and self.start == (row, col):
                        pygame.gfxdraw.filled_circle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 35,
                            block_size // 2 - 9,
                            (255, 0, 0),
                        )
                        pygame.gfxdraw.aacircle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 35,
                            block_size // 2 - 9,
                            (255, 0, 0),
                        )
                    elif self.path and (row, col) in self.path and not self.highlight_explored_path:
                        pygame.gfxdraw.filled_circle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 35,
                            block_size // 2 - 9,
                            LIGHT_GRAY,
                        )
                        pygame.gfxdraw.aacircle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 35,
                            block_size // 2 - 9,
                            LIGHT_GRAY,
                        )
                    elif self.obstacles and (row, col) in self.obstacles:
                        pygame.gfxdraw.filled_circle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 35,
                            block_size // 2 - 9,
                            (0, 0, 0),
                        )
                        pygame.gfxdraw.aacircle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 35,
                            block_size // 2 - 9,
                            (0, 0, 0),
                        )
                    elif self.highlight_explored_path and (row, col) in self.explored_path[explored_path_idx]:
                        pygame.gfxdraw.filled_circle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 35,
                            block_size // 2 - 9,
                            LIGHT_GRAY,
                        )
                        pygame.gfxdraw.aacircle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 35,
                            block_size // 2 - 9,
                            LIGHT_GRAY,
                        )

            # shows time taken to run
            text = f"{self.time:.2e}"
            text_surface = font.render(text, True, (0, 0, 0))  # True for anti-aliased text, color is black
            screen.blit(text_surface, (width - text_surface.get_rect().width + 2, 7))

            # Update the display
            pygame.display.flip()

            # ticks the explored path on each frame
            if self.highlight_explored_path and explored_path_idx != -1:
                time.sleep(.05)
                explored_path_idx += 1
                if explored_path_idx >= len(self.explored_path):
                    explored_path_idx = -1

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # runs on main
    start_pos = (0, 0)
    target_pos = (4, 4)
    env = Environment(start_pos, target_pos, True, True)
    env.run_env()
