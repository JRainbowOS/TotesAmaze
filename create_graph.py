import os 
import numpy as np
from skimage.io import imread, imsave
from node import Node 
from network import Network
from solver import Solver

class Maze:

    BITMAP_DIR = os.path.join(os.getcwd(), 'bitmaps')

    def __init__(self, maze_type, maze_size):
        self.maze_size = maze_size 
        self.maze_type = maze_type
        self.bmp, self.height, self.width = self.get_bmp()
        self.horz_nodes = []
        self.vert_nodes = []
        self.node_ids = []

    def get_bmp(self):
        """
        NB wall is black (0) and path is white (255)
        """
        bmp_path = os.path.join(Maze.BITMAP_DIR, self.maze_type, f'{self.maze_size}.bmp')
        assert os.path.exists(bmp_path), 'Maze not found :( '
        bmp = imread(bmp_path)
        height, width = bmp.shape
        return bmp, height, width 

    def add_node(self, position, row, col):
        pass

    def bmp_to_graph(self):
        bmp, height, width = self.bmp, self.height, self.width  

        # 1a. find start and add node and mark within 'top_nodes'
        # 1b. find end and add node and attribute 'vert' (SKIP THIS)
        # 2a. for each row, locate potential nodes (all junctions and dead ends)
        # 2b. connect any horizontal edges between nodes on row 
        # 2c. update top_node list for all nodes which have southerly paths
        # 2d. connect bottom_nodes to nearest top_node above  

        # vert_nodes = []
        horz_nodes = []
        network = Network()
        node_ids = []

        # 1. 
        # Create Start Node
        start_row = 0
        start_id = 0
        # start_col = bmp[start_row].index(255)
        start_col = np.where(bmp[start_row] == 255)[0][0]
        start_node = Node(start_id, row=start_row, col=start_col, position='start')
        node_ids.append(start_id)
        network.nodes[0].mark_position('start')

        # Create top_nodes structure
        # top_nodes = [-1] * self.width
        # list of lists of form [node_id, row]
        top_nodes = [[None, None]] * self.width
        top_nodes[start_col] = [start_id, start_row]

        # 2. 
        node_ids = [0]
        iters = 0
        for r in range(1, height - 1):
            # CURRENTLY ASSUMES THERE IS A WALL AROUND THE WHOLE MAZE APART FROM TWO EXITS
            left_node = None
            left_col = None
            for c in range(0, width):
                # WALL IS 0; PATH IS 255
                iters += 1
                print(f'iteration: {iters}')
                print(f'cell_row: {r}, cell_col: {c}, cell_value: {bmp[r][c]}')
                # left_node = None
                # left_col = None

                # WALL 
                # ignore
                if bmp[r][c] == 0:
                    print('wall!')
                    continue                

                # WALL PATH PATH
                # beginning of corridor (add and check if vert too)
                if bmp[r][c - 1] == 0 and bmp[r][c] == 255 and bmp[r][c + 1] == 255:
                    print('WPP')
                    new_node_id = node_ids[-1] + 1
                    new_node = Node(new_node_id, row=r, col=c)
                    network.add_node(new_node_id)
                    node_ids.append(new_node_id)
                    print('creating new left_node')
                    left_node = new_node_id
                    print(f'left node is now: {left_node}')
                    left_col = c 
                    if bmp[r - 1][c] == 0 and bmp[r + 1][c] == 0:
                        # i.e. wall above and below 
                        continue
                    elif bmp[r - 1][c] == 255 and bmp[r + 1][c] == 255:
                        # i.e. paths above and below
                        node_above_id, node_above_row = top_nodes[c]
                        distance = r - node_above_row
                        new_node.add_connection(node_above_id, weight=distance)
                        network.add_path(start_node_id=new_node_id, end_node_id=node_above_id, weight=distance)
                        top_nodes[c] = [new_node_id, r]
                    elif bmp[r - 1][c] == 0 and bmp[r + 1][c] == 255:
                        # i.e. wall above and path below
                        top_nodes[c] = [new_node_id, r] 
                    elif bmp[r - 1][c] == 255 and bmp[r + 1][c] == 0:
                        # i.e. path above and wall below
                        node_above_id, node_above_row = top_nodes[c]
                        print(f'node_above_row: {node_above_row}')
                        distance = r - node_above_row
                        new_node.add_connection(node_above_id, weight=distance)
                        network.add_path(start_node_id=new_node_id, end_node_id=node_above_id, weight=distance)
                        top_nodes[c] = [-1, None]


                # WALL PATH WALL
                # ignore unless wall below (add to vert nodes)
                if bmp[r][c - 1] == 0 and bmp[r][c] == 255 and bmp[r][c + 1] == 0:
                    print('WPW')
                    left_node = None
                    left_col = None
                    if bmp[r - 1][c] == bmp[r + 1][c]:
                        # i.e. wall above and below or path above and below
                        # in a perfect maze you shouldn't get path surrounded by wall on all sides
                        continue
                    elif bmp[r - 1][c] == 0 and bmp[r + 1][c] == 255:
                        # i.e. wall above and path below
                        new_node_id = node_ids[-1] + 1
                        new_node = Node(new_node_id, row=r, col=c)
                        network.add_node(new_node_id)
                        node_ids.append(new_node_id)
                        top_nodes[c] = [new_node_id, r] 
                    elif bmp[r - 1][c] == 255 and bmp[r + 1][c] == 0:
                        # i.e. path above and wall below
                        node_above_id, node_above_row = top_nodes[c]
                        distance = r - node_above_row
                        new_node.add_connection(node_above_id, weight=distance)
                        network.add_path(start_node_id=new_node_id, end_node_id=node_above_id, weight=distance)
                        top_nodes[c] = [None, None]

                # PATH PATH WALL
                # end of corridor (and and check if vert too)
                if bmp[r][c - 1] == 255 and bmp[r][c] == 255 and bmp[r][c + 1] == 0:
                    print('PPW')
                    new_node_id = node_ids[-1] + 1
                    new_node = Node(new_node_id, row=r, col=c)
                    network.add_node(new_node_id)
                    node_ids.append(new_node_id)
                    print(f'connecting right node {new_node_id} to left node {left_node}')
                    new_node.add_connection(left_node, c - left_col)
                    network.add_path(new_node_id, left_node, weight=c-left_col)
                    print('destroying left node')
                    left_node = None
                    left_col = None
                    if bmp[r - 1][c] == 255 and bmp[r + 1][c] == 255:
                        # i.e. end of corridor but with paths above and below
                        node_above_id, node_above_row = top_nodes[c]
                        distance = r - node_above_row
                        new_node.add_connection(node_above_id, weight=distance)
                        network.add_path(start_node_id=new_node_id, end_node_id=node_above_id, weight=distance)
                        top_nodes[c] = [new_node_id, r]
                    if bmp[r - 1][c] == 0 and bmp[r + 1][c] == 0:
                        # i.e. dead end of corridor
                        continue
                    elif bmp[r - 1][c] == 0 and bmp[r + 1][c] == 255:
                        # i.e. wall above and path below
                        new_node_id = node_ids[-1] + 1
                        new_node = Node(new_node_id, row=r, col=c)
                        network.add_node(new_node_id)
                        node_ids.append(new_node_id)
                        top_nodes[c] = [new_node_id, r]                         
                    elif bmp[r - 1][c] == 255 and bmp[r + 1][c] == 0:
                        # i.e. path above and wall below
                        node_above_id, node_above_row = top_nodes[c]
                        distance = r - node_above_row
                        new_node.add_connection(node_above_id, weight=distance)
                        network.add_path(start_node_id=new_node_id, end_node_id=node_above_id, weight=distance)
                        top_nodes[c] = [None, None]
                        
                # PATH PATH PATH 
                # middle of corridor (check if vert node)
                if bmp[r][c - 1] == 255 and bmp[r][c] == 255 and bmp[r][c + 1] == 255:
                    print('PPP')
                    if bmp[r - 1][c] == 0 and bmp[r + 1][c] == 0:
                        # both wall
                        continue
                    if bmp[r - 1][c] == 255 and bmp[r + 1][c] == 255:
                        # crossroads
                        new_node_id = node_ids[-1] + 1
                        new_node = Node(new_node_id, row=r, col=c)
                        network.add_node(new_node_id)
                        node_ids.append(new_node_id)
                        node_above_id, node_above_row = top_nodes[c]
                        distance = r - node_above_row
                        new_node.add_connection(node_above_id, weight=distance)
                        network.add_path(start_node_id=new_node_id, end_node_id=node_above_id, weight=distance)
                        top_nodes[c] = [new_node_id, r]
                    if bmp[r - 1][c] == 255 and bmp[r + 1][c] == 0:
                        # T-Junction (North / West / East)
                        new_node_id = node_ids[-1] + 1
                        new_node = Node(new_node_id, row=r, col=c)
                        network.add_node(new_node_id)
                        node_ids.append(new_node_id)
                        node_above_id, node_above_row = top_nodes[c]
                        distance = r - node_above_row
                        new_node.add_connection(node_above_id, weight=distance)
                        network.add_path(start_node_id=new_node_id, end_node_id=node_above_id, weight=distance)
                        top_nodes[c] = [None, None]
                    if bmp[r - 1][c] == 0 and bmp[r + 1][c] == 255:
                        # T-Junction (South / West / East)
                        new_node_id = node_ids[-1] + 1
                        new_node = Node(new_node_id, row=r, col=c)
                        network.add_node(new_node_id)
                        node_ids.append(new_node_id)
                        top_nodes[c] = [new_node_id, r]

        # add end node
        end_row = self.height - 1
        end_id = node_ids[-1] + 1
        end_col = np.where(bmp[end_row] == 255)[0][0]
        end_node = Node(end_id, row=end_row, col=end_col, position='end')
        node_above_id, distance = top_nodes[end_col]
        end_node.add_connection(node_above_id, weight=distance)
        network.add_path(start_node_id=node_above_id, end_node_id=end_id, weight=distance)

        return network         
                                                


def main():
    MAZE_TYPE = 'perfect'
    MAZE_SIZE = '15'
    maze = Maze(maze_type=MAZE_TYPE, maze_size=MAZE_SIZE)
    bmp, _, _ = maze.get_bmp()
    
    network = maze.bmp_to_graph()
    network.mark_end(network.node_ids[-1])

    solver = Solver('dijkstra')
    solution = solver.solve(network)
    print(f'Minimal distance is {solution[0]}, spanning nodes {solution[1]}')

    print(network)

if __name__ == '__main__':
    main()
    

