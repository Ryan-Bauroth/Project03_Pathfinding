import pygame
from pygame import gfxdraw
import sys

from alg import AStar

# Set up screen dimensions
dimensions = (10, 10)
block_size = 40
width, height = dimensions[0] * block_size, dimensions[1] * block_size

# Set up display
screen = pygame.display.set_mode((width + 10, height + 10))
pygame.display.set_caption('A* Board')

# Define colors
BACKGROUND_COLOR = (247, 247, 247)
LIGHT_GRAY = (180, 180, 180)

class Environment:
    def __init__(self, start_pos, target_pos, diagonal=False):
        self.start = start_pos
        self.target = target_pos
        self.grid = [[0 for _ in range(dimensions[0])] for _ in range(dimensions[1])]
        self.obstacles = []
        self.path = []
        self.diagonal = diagonal


    def update_path(self):
        alg = AStar(self.grid, self.start, self.target, self.diagonal)
        self.path = alg.find_path()

    def update_obstacles(self, grid):
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == 1:
                    self.obstacles.append((row, col))

    def run_env(self):
        # Initialize Pygame
        pygame.init()

        self.update_path()
        self.update_obstacles(self.grid)

        # Run the game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        col = pos[0] // block_size
                        row = pos[1] // block_size
                        self.grid[row][col] = 1 - self.grid[row][col]
                        self.update_obstacles(self.grid)
                        self.update_path()

            # Fill the background
            screen.fill(BACKGROUND_COLOR)

            # Draw the chessboard blocks
            for row in range(10):
                for col in range(10):
                    rect = pygame.Rect(col * block_size + 5, row * block_size + 5, block_size, block_size)
                    full_rect = pygame.Rect(5, 5, width, height)
                    # Add an outline to each square
                    pygame.draw.rect(screen, LIGHT_GRAY, full_rect, 2)
                    pygame.draw.rect(screen, LIGHT_GRAY, rect, 1)

                    if self.target and self.target == (row, col):
                        pygame.gfxdraw.aacircle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 5,
                            block_size // 2 - 9,
                            (0, 255, 0),
                        )
                        pygame.gfxdraw.filled_circle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 5,
                            block_size // 2 - 9,
                            (0, 255, 0),
                        )
                    elif self.start and self.start == (row, col):
                        pygame.gfxdraw.filled_circle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 5,
                            block_size // 2 - 9,
                            (255, 0, 0),
                        )
                        pygame.gfxdraw.aacircle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 5,
                            block_size // 2 - 9,
                            (255, 0, 0),
                        )
                    elif self.path and (row, col) in self.path:
                        pygame.gfxdraw.filled_circle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 5,
                            block_size // 2 - 9,
                            LIGHT_GRAY,
                        )
                        pygame.gfxdraw.aacircle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 5,
                            block_size // 2 - 9,
                            LIGHT_GRAY,
                        )
                    elif self.obstacles and (row, col) in self.obstacles:
                        pygame.gfxdraw.filled_circle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 5,
                            block_size // 2 - 9,
                            (0, 0, 0),
                        )
                        pygame.gfxdraw.aacircle(
                            screen,
                            col * block_size + block_size // 2 + 5,
                            row * block_size + block_size // 2 + 5,
                            block_size // 2 - 9,
                            (0, 0, 0),
                        )

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    start_pos = (0, 0)
    target_pos = (4, 4)
    env = Environment(start_pos, target_pos, True)
    env.run_env()
