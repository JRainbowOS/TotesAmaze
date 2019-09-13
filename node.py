class Node:

    def __init__(self, id, position='middle', visited=False):
        self.id = id
        self.connections = {}
        self.position = position
        self.visited = visited
        self.distance = float('inf')
    
    def __repr__(self):
        return f'Node({self.id})'

    def mark_visited(self, visited):
        """
        expects 'visited' to be a Boolean
        """
        self.visited = visited

    def mark_position(self, position):
        assert position in ('start', 'end', 'middle')
        self.position = position
        if position == 'start':
            self.distance = 0 

    def add_connection(self, new_node_id, weight):
        self.connections[new_node_id] =  weight

    def change_distance(self, new_distance):
        self.distance = new_distance

