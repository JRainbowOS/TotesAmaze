from solver import Solver
from network import Network

def dijkstra(network):
    """
    Implementation of Dijktra's algorithm for solving path
    """
    # assert isinstance(network, Network), 'network is not from Network class'
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
    total_distance = 0

    # algorithm terminates when every node has been visited
    while not network.nodes[end_id].visited:
        # 1. consider unvisited neighbours and calculate tentative distance via current node
        # 2. compare tentative distances of neighbouring nodes with current distances and assign the smaller
        # 3. mark the current node as visited and remove from unvisited set
        # 4. if end node is marked as visited or smallest distances in unvisited set is inf, break
        # 5. else select unvisited node with smallest distance and set as new current node
        
        unvisited_neighbours = network.find_unvisited_neighbours(current_position_id)
        for unvisited_id in unvisited_neighbours:
            connection_distance = network.nodes[current_position_id].connections[unvisited_id]
            current_distance = total_distance + connection_distance
            node_distance = network.nodes[unvisited_id].distance
            if current_distance < node_distance:
                print(f'changing distance from {node_distance} to {current_distance}')
                network.nodes[unvisited_id].change_distance(current_distance)
        network.nodes[current_position_id].visited = True
        unvisited.remove(current_position_id)

        if network.find_smallest_distance_in_node_set(unvisited) == float('inf'):
            # Or should this really be added to the while statement?
            break





        


        break

    return start_id, end_id

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
    network.add_path(2,4,3)
    network.add_path(3,6,2)
    network.add_path(5,7,2)
    network.add_path(5,6,3)
    network.add_path(4,7,1)
    network.nodes[7].mark_position('end')    

    solution = dijkstra(network)
    print(solution)

if __name__ == '__main__':
    main()
