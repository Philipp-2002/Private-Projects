import random
import Node
import Edge


#every connection has to be EXACTLY once in every graph datastructure.
#This is because the adjacence list takes each directed edge and transforms it into
#an undirected edge by adding (b, a) to the existing (a, b) edge




def fullGraph(nodeNum):
    nodes = []
    edges = []

    for i in range(nodeNum):
        nodes.append(Node.Node(random.randint(0,800), random.randint(0,800)))
        for j in range(nodeNum):
            if i != 0:
                edges.append(Edge.Edge(i,j))

    return (nodes, edges)


def gridGraph(nodeNumY, nodeNumX):
    nodes = []
    edges = []
    distX = 700/nodeNumX
    distY = 700/nodeNumY
    nodeCounter = 0
    
    for y in range(nodeNumY):
        for x in range(nodeNumX):
            nodes.append(Node.Node(50+distX*x, 50+distY*y))
            if x != nodeNumX-1: #node darunter 
                edges.append(Edge.Edge(nodeCounter, nodeCounter+1))
            if y != nodeNumY-1: #node darunter
                edges.append(Edge.Edge(nodeCounter, nodeCounter+nodeNumX))

            nodeCounter += 1
    return (nodes, edges)

def gridGraph2(nodeNumY, nodeNumX):
    nodes = []
    edges = []
    distX = 700/nodeNumX
    distY = 700/nodeNumY
    nodeCounter = 0
    
    for y in range(nodeNumY):
        for x in range(nodeNumX):
            nodes.append(Node.Node(50+distX*x, 50+distY*y))

            if y % 2 == 0:
                if x != nodeNumX-1: #node darunter 
                    edges.append(Edge.Edge(nodeCounter, nodeCounter+1))

            if y != nodeNumY-1: #node darunter
                edges.append(Edge.Edge(nodeCounter, nodeCounter+nodeNumX))

            nodeCounter += 1
    return (nodes, edges)






def triangleGridGraph(nodeNumY, nodeNumX):
    nodes = []
    edges = []
    distX = 700/nodeNumX
    distY = 700/nodeNumY
    nodeCounter = 0
    
    for y in range(nodeNumY):
        addNode = 0
        if y % 2 == 0:
            addNode = 1

            
        for x in range(nodeNumX+addNode):
            if y % 2 == 0:
                nodes.append(Node.Node(50-distX/2+distX*x, 50+distY*y))
            else:
                nodes.append(Node.Node(50+distX*x, 50+distY*y))

            if x  != nodeNumX+addNode-1: #node rechts davon
                edges.append(Edge.Edge(nodeCounter, nodeCounter+1))

            if y != nodeNumY-1:
                if x != nodeNumX:
                    edges.append(Edge.Edge(nodeCounter, nodeCounter+nodeNumX+1))
##                if x >= 2 and x != nodeNumX:
##                    newEdge = Edge.Edge(nodeCounter-1, nodeCounter+nodeNumX+1)
##                    edges.append(newEdge)
                    
            nodeCounter += 1
            
    return (nodes, edges)  

def randomGraph(nodeNum, averageNeighborNum):
    nodes = []
    edges = []

    for i in range(nodeNum):
        newNode = Node.Node(random.randint(0, 800), random.randint(0, 800))
        nodes.append(newNode)
    

    for i in range(nodeNum):
        for n in range(max(1, int(random.gauss(averageNeighborNum, 1)))):
            while True:
                newEdge = [i, random.randint(0, nodeNum-1)]
                if newEdge[0] != newEdge[1]: #connection between the same node
                    if newEdge not in edges and reversed(Edge) not in edges:
                        edges.append(newEdge)
                        break
    for i in range(len(edges)):
        edges[i] = Edge.Edge(edges[i][0], edges[i][1])
    return (nodes,edges)
        
def greedyRingGraph(nodeNum):
    nodes = []
    connections = []

    for i in range(nodeNum):
        newNode = Node.Node(random.randint(0, 800), random.randint(0, 800))
        nodes.append(newNode)
    
    
    notVisitedNodes = list(range(nodeNum))

    
    currentNode = 0
    for i in range(nodeNum-1):
        notVisitedNodes.remove(currentNode)

        nearestDistance = 1000000
        nearestNode = None
        for nextNode in notVisitedNodes:
            distance = ((nodes[currentNode].x-nodes[nextNode].x)**2+(nodes[currentNode].y-nodes[nextNode].y)**2)**.5
            if distance < nearestDistance:
                nearestDistance = distance
                nearestNode = nextNode


        connections.append([currentNode,nearestNode])
        currentNode = nearestNode
    connections.append([currentNode, 0]) #connect last and first node
               
    return (nodes,connections)



