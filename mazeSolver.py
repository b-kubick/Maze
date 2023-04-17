import heapq


class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.height = maze.height
        self.width = maze.width
        self.predecessor = [[None] * self.width for _ in range(self.height)]
        
    # calculates the manhattan distance between the current cell(row, col) and the goal cell(goal_row, goal_col)
    def heuristic(self, row, col):
        goal_row, goal_col = self.maze.goal
        return abs(row - goal_row) + abs(col - goal_col)

    def solve(self):
        start_row, start_col = self.maze.start
        open_list = [(0, start_row, start_col)]  # Priority queue with (priority, row, col) tuples
        heapq.heapify(open_list)

        g_costs = [[float("inf")] * self.width for _ in range(self.height)]
        g_costs[start_row][start_col] = 0

        while open_list:
            _, current_row, current_col = heapq.heappop(open_list)

            if (current_row, current_col) == self.maze.goal:
                break

            for neighbor_row, neighbor_col in self.maze.get_neighbors(current_row, current_col):
                tentative_g_cost = g_costs[current_row][current_col] + 1

                if tentative_g_cost < g_costs[neighbor_row][neighbor_col]:
                    g_costs[neighbor_row][neighbor_col] = tentative_g_cost
                    f_cost = tentative_g_cost + self.heuristic(neighbor_row, neighbor_col)
                    heapq.heappush(open_list, (f_cost, neighbor_row, neighbor_col))
                    self.predecessor[neighbor_row][neighbor_col] = (current_row, current_col)

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