class Edge:
    def __init__(self, n1, n2, distance):
        self.__pair = (n1, n2)
        self.distance = distance

    def get_neighbour(self, node):
        if node not in self.__pair:
            return None
        if self.__pair[0] == node:
            return self.__pair[1]
        return self.__pair[0]