from maze import Maze
from mazeSolver import MazeSolver
from mazeGUI import MazeGUI
import random

def main():
    x = 15
    y = 15
    start=(random.randint(0,x-1 ), random.randint(0, y-1)) 
    goal=(random.randint(0, x-1), random.randint(0, y-1))
    
    # Create a maze with default width of 15 and random start and goal points
    maze = Maze(x, y, start, goal)
    
    solver = MazeSolver(maze)
    # Create a MazeGUI object with the default maze, solver, and cell size
    gui = MazeGUI(maze, solver)

if __name__ == "__main__":
    # shows the full grid
    #width, height = 15, 15
    #adjusts the goal
    #start, goal = (1, 1), (13, 13)
    main()

 