class Node:

    def __init__(self, id, row=None, col=None, position='middle', visited=False):
        self.id = id
        self.row = row
        self.col = col 
        self.connections = {}
        self.position = position
        # self.visited = visited
        self.distance = float('inf')
        # self.previous = None
        self.vert = False 
    
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

    def mark_vert(self):
        self.vert = True 

    def add_connection(self, new_node_id, weight):
        self.connections[new_node_id] =  weight

    def change_distance(self, new_distance):
        self.distance = new_distance

