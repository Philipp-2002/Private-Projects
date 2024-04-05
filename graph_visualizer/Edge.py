
class Edge:
    n1 = None
    n2 = None
    status = "unvisited"

    def __init__(self, n1Id, n2Id):
        self.n1 = n1Id
        self.n2 = n2Id
        self.status = "unvisited"


