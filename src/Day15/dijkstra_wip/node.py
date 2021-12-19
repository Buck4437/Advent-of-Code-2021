class Node:
    def __init__(self, key=""):
        self.id = key
        self.edges = set()
        self.distance = 0

    def add_edge(self, edge):
        self.edges.add(edge)

    def __str__(self):
        return "Node " + self.id
