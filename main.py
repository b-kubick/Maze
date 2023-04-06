from maze import Maze
from mazeSolver import MazeSolver
from mazeGUI import MazeGUI

if __name__ == "__main__":
    width, height = 10, 10
    start, goal = (1, 1), (8, 8)

    maze = Maze(width, height, start, goal)
    solver = MazeSolver(maze)

    gui = MazeGUI(maze, solver)