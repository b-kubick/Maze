class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.height = maze.height
        self.width = maze.width
        self.distance = [[float("inf")] * self.width for _ in range(self.height)]
        self.predecessor = [[None] * self.width for _ in range(self.height)]

    def initialize_single_source(self):
        start_row, start_col = self.maze.start
        self.distance[start_row][start_col] = 0

    def relax(self, current, neighbor):
        row, col = current
        n_row, n_col = neighbor
        if self.distance[n_row][n_col] > self.distance[row][col] + 1:
            self.distance[n_row][n_col] = self.distance[row][col] + 1
            self.predecessor[n_row][n_col] = current

    def solve(self):
        self.initialize_single_source()
        for _ in range(self.height * self.width):
            for row in range(self.height):
                for col in range(self.width):
                    current = (row, col)
                    if self.maze.is_valid_coordinate(row, col):
                        for neighbor in self.maze.get_neighbors(row, col):
                            self.relax(current, neighbor)

    def get_solution_path(self):
        path = []
        current = self.maze.goal

        while current is not None:
            path.append(current)
            row, col = current
            current = self.predecessor[row][col]

        return path[::-1]

    def display_solution(self):
        solution_path = self.get_solution_path()
        self.maze.display(solution_path)
        
    def reset(self):
        self.solution_path = []
        self.visited = set()
        self.found_solution = False