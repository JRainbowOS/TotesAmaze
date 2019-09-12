# from methods import dijkstra

class Solver:

    def __init__(self, method):
        self.method = method

    def solve(self, network):
            if self.method == 'dijkstra':
                solution = dijkstra(network)
            # elif:
            #     other methods go here
            return solution
