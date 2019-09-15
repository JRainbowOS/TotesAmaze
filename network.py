from node import Node
from solver import Solver
import time

def timer(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        print(f'time taken: {end - start}s')
    return inner

class Network:

    def __init__(self):
        self.num_nodes = 1
        self.start_node = Node(0)
        self.start_node.distance = 0 
        self.node_ids = [0]
        self.nodes = [Node(0)]

    def __repr__(self):
        res = ''
        for node in self.nodes:
            res += str(node) + '--'
        return res[:-2]    

    def add_node(self, node_id):
        assert node_id not in self.node_ids, 'node_id already exists!'
        self.num_nodes += 1
        new_node = Node(node_id)
        self.node_ids.append(node_id)
        self.nodes.append(new_node)    
        return new_node

    def add_path(self, start_node_id, end_node_id, weight, debug=False):
        if start_node_id not in self.node_ids:
            # create new start node
            if debug: print('1')
            start_node = self.add_node(start_node_id)
        else:
            if debug: print('2')
            start_node = self.nodes[start_node_id]
        if end_node_id not in self.node_ids:
            # create new end node
            if debug: print('3')
            end_node = self.add_node(end_node_id)
        else:
            if debug: print('4')
            end_node = self.nodes[end_node_id]

        start_node.add_connection(end_node_id, weight)
        end_node.add_connection(start_node_id, weight)

    def mark_end(self, node_id):
        assert node_id in self.node_ids, 'node does not exist!'
        end_node = self.nodes[node_id]
        end_node.mark_position('end')

    def find_unvisited_neighbours(self, current_node_id):
        """
        TODO: make this a list comprehension
        """
        neighbours = list(self.nodes[current_node_id].connections.keys())
        unvisited = []
        for n in neighbours:
            if not self.nodes[n].visited:
                unvisited.append(n)
        return unvisited

    def find_smallest_distance_in_node_set(self, list_of_node_ids):
        """
        TODO: This should probably use np.argmin and a list comprehension
        """
        # distances = []
        # for n in list_of_node_ids:
        #     distances.append(self.nodes[n].distance)
        # return list_of_node_ids.index(min(distances)), min(distances)

        min_distance = float('inf')
        min_node_id = -1
        for n in list_of_node_ids:
            distance = self.nodes[n].distance
            if distance < min_distance:
                min_distance = distance
                min_node_id = n
        # if min_node_id == -1:
        #     raise Exception('all distances are infinite!')
        return min_node_id, min_distance

    def propagate_tree(self, end_id):
        path_from_end = [end_id]
        current_node = self.nodes[end_id]
        while current_node is not None:
            if current_node.previous is None:
                break 
            else:
                previous_node = self.nodes[current_node.previous]
                path_from_end.insert(0, current_node.previous)
                current_node = previous_node
        return path_from_end
        
@timer
def main():
    network = Network()
    network.nodes[0].mark_position('start')
    network.add_path(0,1,3)
    network.add_path(0,2,1)
    network.add_path(0,3,2)
    network.add_path(1,4,3)
    network.add_path(1,3,4)
    network.add_path(2,5,6)
    network.add_path(2,6,5)
    network.add_path(3,4,3)
    network.add_path(3,6,2)
    network.add_path(5,7,2)
    network.add_path(5,6,3)
    network.add_path(4,7,1)
    network.nodes[7].mark_position('end')    

    print(network)

    solver = Solver('dijkstra')
    solution = solver.solve(network)
    print(f'minimal distance is {solution[0]} spanning nodes {solution[1]}')

if __name__ == '__main__':
    main()
