from solver import Solver
from network import Network
import time

def dijkstra(network):
    """
    Implementation of Dijktra's algorithm for solving path
    """
    # First check that network has exactly one start and end point and find unvisited nodes
    start_id = -1
    end_id = -1
    unvisited = []
    for node in network.nodes:
        if node.position == 'start':
            start_id = node.id
        if node.position == 'end':
            end_id = node.id
        if not node.visited:
            unvisited.append(node.id)

    assert start_id != end_id != -1, 'start / end either non-existent or the same!' # TODO: check logic

    current_position_id = start_id

    # algorithm terminates when end node has been visited
    while not network.nodes[end_id].visited:
        # 1. consider unvisited neighbours and calculate tentative distance via current node
        # 2. compare tentative distances of neighbouring nodes with current distances and assign the smaller
        # 3. mark the current node as visited and remove from unvisited set
        # 4. if end node is marked as visited or smallest distances in unvisited set is inf, break
        # 5. else select unvisited node with smallest distance and set as new current node
        
        unvisited_neighbours = network.find_unvisited_neighbours(current_position_id)
        for unvisited_id in unvisited_neighbours:
            current_distance = network.nodes[current_position_id].distance
            connection_distance = network.nodes[current_position_id].connections[unvisited_id]
            alternative_distance = current_distance + connection_distance
            if alternative_distance < network.nodes[unvisited_id].distance:
                network.nodes[unvisited_id].distance = alternative_distance
                network.nodes[unvisited_id].previous = current_position_id

        network.nodes[current_position_id].visited = True
        unvisited.remove(current_position_id)

        new_position_id, smallest_distance = network.find_smallest_distance_in_node_set(unvisited)

        if smallest_distance == float('inf'):
            print('all remaining unvisited nodes have infinite distance!')
            break

        else:
            current_position_id = new_position_id
        
    path = network.propagate_tree(end_id)

    return network.nodes[end_id].distance, path

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

    solution = dijkstra(network)
    print(f'Minimal distance is {solution[0]}, spanning nodes {solution[1]}')

if __name__ == '__main__':
    main()
