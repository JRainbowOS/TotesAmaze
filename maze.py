from cell import Cell
from random import choice

class Maze:

    def __init__(self, width, height, start_cell_row, start_cell_col):
        assert start_cell_row < height and start_cell_col < width, 'start cell out of range!'
        self.width = width
        self.height = height
        self.start_cell_row = start_cell_row
        self.start_cell_col = start_cell_col
        self.grid = self.initialise_grid()

    def __repr__(self):
        return f'Maze({self.width}, {self.height})'

    def initialise_grid(self):
        maze_cells = []
        for r in range(self.height):
            maze_rows = []
            for c in range(self.width):
                cell = Cell(r, c, self.height, self.width)
                maze_rows.append(cell)
            maze_cells.append(maze_rows)

        maze_cells[self.start_cell_row][self.start_cell_col].mark_visited()
        print(maze_cells)
        return maze_cells

    def random_walk_maze_generator(self):
        unvisited = [[r, c] for r in range(self.height) for c in range(self.width)]
        unvisited.remove([self.start_cell_row, self.start_cell_col])
        iters = 0
        while unvisited:
            new_path_start_row, new_path_start_col = choice(unvisited)
            new_path_start_cell = self.grid[new_path_start_row][new_path_start_col]
            print(new_path_start_cell)
            iters += 1
            if iters > 5:
                break



def main():
    maze = Maze(6, 6, 5, 3)
    # print(maze.width)
    # cells = maze.initialise_grid()
    # print(cells)
    maze.random_walk_maze_generator()

if __name__ == '__main__':
    main()