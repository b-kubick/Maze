import tkinter as tk
import random

from mazeSolver import MazeSolver

class MazeGUI:
    def __init__(self, maze, solver, cell_size=30):
        self.maze = maze
        self.solver = solver
        self.cell_size = cell_size

        self.root = tk.Tk()
        self.solved = tk.BooleanVar()
        self.solved.set(False)

        self.canvas = tk.Canvas(self.root, width=maze.width * cell_size, height=maze.height * cell_size)
        self.canvas.pack()

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve_and_draw_solution)
        self.solve_button.pack()

        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.generate_maze)
        self.refresh_button.pack()

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_app)
        self.exit_button.pack()

        self.generate_maze()
        self.root.mainloop()

    def draw_maze(self):
        for i, row in enumerate(self.maze.grid):
            for j, cell in enumerate(row):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                if (i, j) == self.maze.start:
                    color = "red"
                elif (i, j) == self.maze.goal:
                    color = "green"
                elif cell == 1:
                    color = "black"
                else:
                    color = "white"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        if self.solved.get():
            self.draw_solution(self.solver.get_solution_path())

    def solve_and_draw_solution(self):
        if not self.solved.get():
            self.solver.solve()
            self.draw_solution(self.solver.get_solution_path())
            self.solve_button.config(text="Clear")
            self.solved.set(True)
        else:
            self.canvas.delete("path")
            self.solve_button.config(text="Solve")
            self.solved.set(False)
            self.solver.reset()  # Reset the solver when clearing the solution

    def draw_solution(self, solution_path):
        for i, (row, col) in enumerate(solution_path):
            x1, y1 = col * self.cell_size, row * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size

            if (row, col) == self.maze.start:
                color = "red"  # Start position
            elif (row, col) == self.maze.goal:
                color = "green"  # Exit position
            else:
                color = "brown"  # Solution path

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="path")

    def generate_maze(self):
        self.maze.generate_maze()
        self.solver = MazeSolver(self.maze)  # Reset the solver's internal state
        # self.solver.maze = self.maze
        self.solved.set(False)
        self.solve_button.config(text="Solve")
        self.canvas.delete("path")
        self.draw_maze()

    def exit_app(self):
        self.root.destroy()