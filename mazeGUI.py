import tkinter as tk
from tkinter import SUNKEN
from tkinter import W
from tkinter import BOTTOM
from tkinter import X

from mazeSolver import MazeSolver

class MazeGUI:
    def __init__(self, maze, solver, cell_size=30):
         # Initialize the MazeGUI class with the specified maze, solver, and cell size
        self.maze = maze
        self.solver = solver
        self.cell_size = cell_size
        self.goal_set = False
        
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
        
        # add a label to the bottom of the GUI window and update its text when the maze is solved.
        self.status_text = tk.StringVar()
        status_label = tk.Label(self.root, textvariable=self.status_text, bd=1, relief=SUNKEN, anchor=W)
        status_label.pack(side=BOTTOM, fill=X)
        
        # Bind the click event to set_goal_cell method
        self.canvas.bind("<Button-1>", self.set_goal_cell)

        # Generate and draw the initial maze
        self.generate_maze()
        
        # Start the main event loop for the GUI
        self.root.mainloop()
        
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

                if self.goal_set and (i, j) == self.maze.goal:
                    color = "yellow"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        
        # Add a border around the maze
        x1, y1 = 0, 0
        x2, y2 = self.maze.width * self.cell_size, self.maze.height * self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2)
        
        if self.solved.get():
            self.draw_solution(self.solver.get_solution_path())

    def solve_and_draw_solution(self):
        
        self.status_text.set("") # clear the status text
        # Solve the maze and redraw the canvas with the solution
        if not self.solved.get():
            self.solver.solve()
            self.draw_solution(self.solver.get_solution_path())
            self.solve_button.config(text="Clear")
            self.solved.set(True)
            self.status_text.set("Maze Solved!")
        else:
            self.canvas.delete("path")
            self.solve_button.config(text="Solve")
            self.solved.set(False)
            self.solver.reset()  # Reset the solver when clearing the solution
    
    def set_goal_cell(self, event):
        
        self.status_text.set("") # clear the status text
        # Get the x and y coordinates of the clicked cell
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        # Check that the clicked cell is valid
        
       # Check that the clicked cell is valid
        if self.maze.grid[y][x] != 1 and (y, x) != self.maze.start:
            # Set the goal cell and redraw the maze
            self.maze.goal = (y, x)
            self.goal_set = True
            self.draw_maze()
            
            # Set the goal cell and redraw the maze
            self.maze.goal = (y, x)
            self.goal_set = True
            self.draw_maze()
            
            # Reset the solve button text
            self.canvas.delete("path")
            self.solve_button.config(text="Solve")
            self.solved.set(False)
        else:
            # Display "Invalid cell" at the bottom
            self.status_text.set("Invalid cell!!")
    
    def update_goal_point(self, event):
        # Convert the coordinates of the mouse click to cell coordinates
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        
        self.status_text.set("") # clear the status text

        # Check if the new goal point is different from the current goal point
        if (x, y) != self.maze.goal and (y, x) != self.maze.start and (y, x) != self.maze.goal:
        # Update the goal point of the maze to the clicked cell
            # Update the goal point of the maze to the clicked cell
            self.maze.goal = (x, y)

            # Clear the canvas and redraw the maze with the updated goal point
            self.canvas.delete("all")
            self.draw_maze()
            self.status_text.set("") # clear the status text
            
            # Reset the solve button text
            
            
        else:
            self.status_text.set("Invalid goal!!")

        # Solve the updated maze and highlight the solution path
        #self.solver.solve()
        #self.highlight_path()
    
        
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