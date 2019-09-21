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
        maze_cells[self.start_cell_row][self.start_cell_col].mark_maze_path()
        
        print(maze_cells)
        return maze_cells
    
    def find_unvisited_neighbours(self, cell_row, cell_col):#, wall_cell=False):
        """
        Returns list of unvisited neighbour coordinates. If wall_cell flag is set to True, 
        will only return neighbour coordinates which are currently part of a wall.
        """
        valid_neighbours = self.grid[cell_row][cell_col].valid_neighbours()
        for vn in valid_neighbours:
            vn_cell = self.grid[vn[0]][vn[1]]
            if not vn_cell.visited:
                valid_neighbours.remove(vn)
            # if wall_cell:
            #     if vn_cell.value == 1:
            #         # what if it is already removed?
            #         valid_neighbours.remove(vn)
        return valid_neighbours

    def loop_erased_random_walk(self, current_cell):
        """
        Returns list of cells on a random walk from random start to first maze cell
        """
        # 1. start list of cells
        # 2. while current cell is wall cell 
        # 3. find all valid neighbouring cells
        # 4. choose one at random  
        # 5. if new cell is wall cell then add all path cells to maze and remove from unvisited 
        # 6. else if new cell is in list of cells, we have a loop, so remove loop and continue 
        # 7. else if new cell is unvisited then add to list of cells (path) and repeat from 2. 

        path_of_cells = [current_cell]
        
        return path_of_cells




    def random_walk_maze_generator(self):
        unvisited = [[r, c] for r in range(self.height) for c in range(self.width)]
        unvisited.remove([self.start_cell_row, self.start_cell_col])
        iters = 0
        while unvisited:
            # 1. pick random unvisited cell
            # 2a. if no unvisited neighbours, mark as visited and remove from unvisited
            # 2b. else pick random unvisited neighbour and create random loop-erased walk until reaches maze
            # 3. add path to maze and remove all path cells from visited 
            new_path_start_row, new_path_start_col = choice(unvisited)
            new_path_start_cell = self.grid[new_path_start_row][new_path_start_col]
            print(new_path_start_cell)
            
            unvisited_neighbours = self.find_unvisited_neighbours(new_path_start_row, new_path_start_col)
            if unvisited_neighbours:
                # pick one...
                loop_erased_path_cells = self.loop_erased_random_walk(self.grid[new_path_start_row][new_path_start_col])
                # remove these from unvisited and mark as part of maze
                for c in loop_erased_path_cells:
                    c.mark_visited()
                    unvisited_neighbours.remove([c.row, c.col])
            else:
                # there were no unvisited neighbours
                unvisited.remove([new_path_start_row, new_path_start_col])
                continue


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