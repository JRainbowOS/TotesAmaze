class Cell:

    def __init__(self, row, col, height, width):
        assert (row <= height) and (col <= width), 'Cell out of range!'
        self.row = row
        self.col = col 
        self.height = height
        self.width = width 
        self.visited = False
        self.value = 0

    def __repr__(self):
        """
        Asterisc means cell has been visited already
        """
        if self.visited:
            return f'Cell({self.row}, {self.col}, *)'
        else:
            return f'Cell({self.row}, {self.col})'

    def mark_visited(self):
        self.visited = True

    def mark_maze_path(self):
        self.value = 1

    def valid_neighbours(self):
        """
        Returns adjacent neighbours in all Cardinal directions
        """
        neighbours = []
        if self.row - 1 >= 0:
            neighbours.append([self.row - 1, self.col])
        if self.row + 1 <= self.height:
            neighbours.append([self.row + 1, self.col])
        if self.col - 1 >= 0:
            neighbours.append([self.row, self.col - 1])
        if self.col + 1 <= self.width:
            neighbours.append([self.row, self.col + 1])
        return neighbours

def main():
    cell = Cell(6,5,8,8)
    print(cell)
    neighbours = cell.valid_neighbours()
    print(neighbours)

if __name__ == '__main__':
    main()



