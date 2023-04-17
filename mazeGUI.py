import tkinter as tk
import random

from mazeSolver import MazeSolver

class MazeGUI:
    def __init__(self, maze, solver, cell_size=30):
         # Initialize the MazeGUI class with the specified maze, solver, and cell size
        self.maze = maze
        self.solver = solver
        self.cell_size = cell_size
        
        # Create the root window for the GUI    
        self.root = tk.Tk()
        self.root.title("Maze Solver")
        
        # Set maximum/minimum window size
        self.root.minsize(700, 600)
        
        # Create a BooleanVar to track whether the maze has been solved
        self.solved = tk.BooleanVar()
        self.solved.set(False)
    
        # Calculate the screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate the center coordinates of the screen
        x_center = int(screen_width / 2 - 700 / 2)
        y_center = int(screen_height / 2 - 600 / 2)
        
        # Set the geometry of the root window to center it on the screen
        self.root.geometry(f"700x600+{x_center}+{y_center}")
        
        # Create a canvas to draw the maze
        self.canvas = tk.Canvas(self.root, width=maze.width * cell_size, height=maze.height * cell_size)
        self.canvas.pack()
        
        # Create a button to solve the maze
        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve_and_draw_solution)
        self.solve_button.pack()
        
        # Create a button to generate a new maze
        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.generate_maze)
        self.refresh_button.pack()
        
        # Create a button to exit the application
        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_app)
        self.exit_button.pack()
        
        # Generate and draw the initial maze
        self.generate_maze()
        
        # Start the main event loop for the GUI
        self.root.mainloop()
    
    def goal_reached(self):
        # Display "Maze solved!" in green on the console when the goal is reached
        self.canvas.create_text(self.maze.goal[1] * self.cell_size + self.cell_size // 2,
        self.maze.goal[0] * self.cell_size + self.cell_size // 2, 
        text="Maze solved!", fill="green")
        print("\033[32mMaze solved!\033[0m")
        
    def draw_maze(self): 
        # Draw the maze
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
        
        # Add a border around the maze
        x1, y1 = 0, 0
        x2, y2 = self.maze.width * self.cell_size, self.maze.height * self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2)
        
        if self.solved.get():
            self.draw_solution(self.solver.get_solution_path())

    def solve_and_draw_solution(self):
        # Solve the maze and redraw the canvas with the solution
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
         # Draw the solution on the canvas
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
        self.goal_reached()

    def generate_maze(self):
        # Generate a new maze and redraw the canvas
        self.maze.generate_maze()
        self.solver = MazeSolver(self.maze)  # Reset the solver's internal state
        self.solved.set(False) # Reset the solved flag to False
        self.solve_button.config(text="Solve")
        self.canvas.delete("path")
        self.draw_maze()

    def exit_app(self):
        self.root.destroy()