class Node:

    def __init__(self, id, position='middle'):
        self.id = id
        self.connections = {}
        self.position = position
    
    def __repr__(self):
        return f'Node({self.id})'

    def mark_position(self, position):
        assert position in ('start', 'end', 'middle')
        self.position = position

    def add_connection(self, new_node_id, weight):
        self.connections[new_node_id] =  weight