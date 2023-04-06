import random

class Maze:
    def __init__(self, width, height, start, goal):
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.grid = [[0] * width for _ in range(height)]

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                for j, cell in enumerate(line.strip()):
                    self.grid[i][j] = int(cell)

    def get_neighbors(self, row, column):
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

        for dr, dc in directions:
            new_row, new_col = row + dr, column + dc
            if self.is_valid_coordinate(new_row, new_col):
                neighbors.append((new_row, new_col))

        return neighbors

    def is_valid_coordinate(self, row, column):
        return (
            0 <= row < self.height
            and 0 <= column < self.width
            and self.grid[row][column] != 1
        )

    def display(self, solution_path=None):
        if solution_path is None:
            solution_path = []

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if (i, j) in solution_path:
                    print("x", end="")
                elif cell == 0:
                    print(" ", end="")
                else:
                    print("#", end="")
            print()

    def generate_maze(self):
        # Initialize the grid to walls
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = 1

        # Start from the starting cell
        x, y = self.start
        self.grid[x][y] = 0

        # List to store frontier cells
        frontiers = []

        # Lambda function to find neighboring cells
        neighbors = lambda x, y: [(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)]

        # Add the neighbors of the starting cell to the frontiers list
        for nx, ny in neighbors(x, y):
            if 0 <= nx < self.height and 0 <= ny < self.width:
                frontiers.append((nx, ny, x, y))

        # Randomly select and process frontier cells
        while frontiers:
            fx, fy, px, py = frontiers.pop(random.randint(0, len(frontiers) - 1))

            if self.grid[fx][fy] == 1:
                self.grid[fx][fy] = 0
                self.grid[px + (fx - px) // 2][py + (fy - py) // 2] = 0

                for nx, ny in neighbors(fx, fy):
                    if 0 <= nx < self.height and 0 <= ny < self.width:
                        frontiers.append((nx, ny, fx, fy))

        # Set the start and goal positions
        self.grid[self.start[0]][self.start[1]] = 0
        self.grid[self.goal[0]][self.goal[1]] = 0

