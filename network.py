from node import Node

class Network:

    def __init__(self):
        self.num_nodes = 1
        self.start_node = Node(0)
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


def main():
    network = Network()
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
    print(network.nodes[6].connections)
    print(str(network.nodes[2]))
    print(network)

if __name__ == '__main__':
    main()
