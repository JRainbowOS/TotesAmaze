import numpy as np 
from utils import manhattan_distance

class Maze:

    def __init__(self, width, height, start_cell_x, start_cell_y, end_cell_x, end_cell_y):
        self.width = width
        self.height = height
        self.start_cell_x, self.start_cell_y = start_cell_x, start_cell_y
        self.end_cell_x, self.end_cell_y = end_cell_x, end_cell_y
        self.grid = self.create_initial_grid()

    def create_initial_grid(self):
        start_cell_x, start_cell_y = self.start_cell_x, self.start_cell_y
        end_cell_x, end_cell_y = self.end_cell_x, self.end_cell_y
        assert start_cell_x < self.width, 'start cell is too far right!'
        # TODO: etc...

        grid = np.zeros((self.height, self.width))
        grid[start_cell_y][start_cell_x] = 1
        grid[end_cell_y][end_cell_x] = 1
        dist = manhattan_distance(start_cell_x, start_cell_y, end_cell_x, end_cell_y)
        if dist < 2:
            raise Exception('start is too close to finish!')
        return grid

def main():
    height, width = 5, 4
    maze = Maze(height, width, 1, 3, 2, 0)
    # maze = Maze(height, width, 1, 3, 1, 2)
    print(maze.grid)

if __name__ == '__main__':
    main()