import numpy as np 
from utils import manhattan_distance
from random import choice
import time
import itertools

class Maze:

    def __init__(self, width, height, start_cell_row, start_cell_col, end_cell_row, end_cell_col):
        # TODO: could be replaced with tuple coordinates 
        # TODO: use row / col for x /y for clarity
        self.width = width
        self.height = height
        self.start_cell_row, self.start_cell_col = start_cell_row, start_cell_col
        # self.end_cell_row, self.end_cell_col = end_cell_row, end_cell_col
        self.grid = self.create_initial_grid()

    def create_initial_grid(self):
        start_cell_row, start_cell_col = self.start_cell_row, self.start_cell_col
        # end_cell_row, end_cell_col = self.end_cell_row, self.end_cell_col
        assert start_cell_row < self.height, 'start cell is too far south!'
        # TODO: etc...

        grid = np.zeros((self.height, self.width))
        grid[start_cell_row][start_cell_col] = 1
        # grid[end_cell_row][end_cell_col] = 1
        # dist = manhattan_distance(start_cell_row, start_cell_col, end_cell_row, end_cell_col)
        # if dist < 2:
        #     raise Exception('start is too close to finish!')
        return grid

    def find_cardinal_cells(self, row, col, with_value=0):
        """
        Returns all the valid cells that are 2N, 2W, 2S, 2E from (row, col) with the specified value
        """
        cardinals = []
        if row - 2 >= 0 and (with_value == self.grid[row - 2][col]):
            cardinals.append([row - 2, col])
        if row + 2 < self.height and (with_value == self.grid[row + 2][col]):
            cardinals.append([row + 2, col])
        if col - 2 >= 0 and (with_value == self.grid[row][col - 2]):
            cardinals.append([row, col - 2])
        if col + 2 < self.width and (with_value == self.grid[row][col + 2]):
            cardinals.append([row, col + 2])
        
        return cardinals

    def modify_frontiers(self, cell_row, cell_col, current_frontiers):
        """
        Removes directly adjacent frontiers and adds any new frontiers
        """
        adjacent_cells = []
        for row in range(cell_row - 1, cell_row + 2, 2):
            for col in range(cell_col - 1, cell_col + 2, 2):
                if row >= 0 and row < self.height and col >= 0 and col < self.width:
                    cell = [row, col]
                    adjacent_cells.append(cell)
                    if cell in current_frontiers:
                        print(f'removing cell {cell} from frontier')
                        current_frontiers.remove(cell)       
        # print(f'current_frontiers: {current_frontiers}')
        candidate_frontiers = self.find_cardinal_cells(cell_row, cell_col, with_value=0)
        # print(f'candidate_frontiers: {candidate_frontiers}')

        frontiers_duped = candidate_frontiers + current_frontiers
        frontiers_duped.sort()
        frontiers = list(frontiers_duped for frontiers_duped, _ in itertools.groupby(frontiers_duped))
        
        return frontiers

    def generate_maze(self):
        frontiers = self.find_cardinal_cells(self.start_cell_row, self.start_cell_col, with_value=0)
        print(frontiers)
        # algorithm terminates when there are no longer any frontiers
        iter_count = 0
        while frontiers:
            # 1. select random available frontier
            # 1b. remove choice from frontiers
            # 2. find random associated cardinal with_value=1 (will be at least one)
            # 3. change the value of the cell between the frontier and its origin (from part 2) to 1 (i.e. a path)
            # 4. remove any frontier cells directly adjacent to new path cell
            # 5. add any new frontier cells
            # 6. choose another random available frontier

            print(frontiers)
            frontier = choice(frontiers)
            print(f'frontier: {frontier}')
            frontiers.remove(frontier)
            origin = choice(self.find_cardinal_cells(frontier[0], frontier[1], with_value=1))
            print(f'origin: {origin}')
            new_path_cell = list(np.mean([frontier, origin], axis=0).astype(int))
            print(f'new_path_cell: {new_path_cell}')
            self.grid[new_path_cell[0]][new_path_cell[1]] = 1
            frontiers = self.modify_frontiers(new_path_cell[0], new_path_cell[1], frontiers)

            time.sleep(0.1)
            iter_count += 1

            if iter_count > 100:
                break

        print(self.grid)

        pass

    def generate_random_walk_maze(self):
        unvisited = set[[row, col] for row in range(self.height) for col in range(self.width)]
        print(len(unvisited))
        pass


def main():
    height, width = 7, 6
    # maze = Maze(height, width, 1, 3, 2, 0)
    # maze = Maze(height, width, 6, 2, 0, 4)
    maze = Maze(width, height, 6, 3, 0, 2)
    # maze = Maze(height, width, 1, 3, 1, 2)
    print(maze.grid)
    maze.generate_random_walk_maze()

if __name__ == '__main__':
    main() 