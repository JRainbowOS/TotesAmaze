class Node:

    def __init__(self, id):
        self.id = id
        self.connections = {}
    
    def __repr__(self):
        return f'Node({self.id})'

    def add_connection(self, new_node_id, weight):
        self.connections[new_node_id] =  weight