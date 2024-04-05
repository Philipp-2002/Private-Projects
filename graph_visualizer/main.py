import pygame
import random
import math
import GraphGenerator
import Stack
from copy import deepcopy

screen = pygame.display.set_mode((800, 800))

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)

screen.fill(WHITE)
pygame.display.update()

class Graph:
    def __init__(self, nodes, edges): #constructor for non empty graph
        self.nodes = nodes #(sorted) list of all nodes (index = id) typ [Node]
        self.edges = edges #(unsorted) list of all edges typ [(Int), (Int)]
        self.allNeighborsOf = [[] for i in range(len(self.nodes))] # [[Int]]
        self.edgeMatrix = [[None for i in range(len(self.nodes))] for j in range(len(self.nodes))]#zum Abfragen des Status einer Kante
        
        self.path = [0]
        for e in self.edges:
            self.allNeighborsOf[e.n1].append(e.n2) #save all nodes in adjacencelist
            self.allNeighborsOf[e.n2].append(e.n1)

            self.edgeMatrix[e.n1][e.n2] = e #save all edges in adjacencematrix
            self.edgeMatrix[e.n2][e.n1] = e

    def drawEdge(self, edge):
        if edge.status == "unvisited":
            color = BLUE
        if edge.status == "visited":
            color = GREEN
        if edge.status == "dashed":
            color = BLACK
        pygame.draw.line(screen, color, (self.nodes[edge.n1].x, self.nodes[edge.n1].y),(self.nodes[edge.n2].x, self.nodes[edge.n2].y), 5)

    def drawNode(self, node):
        if node.status == "visited":
            color = GREEN
        if node.status == "unvisited":
            color = RED
        if node.status == "backtracked":
            color = BLUE

            
        pygame.draw.ellipse(screen, color, (node.x-10, node.y-10, 20, 20))
        
    def draw(self):
        for e in self.edges:
            self.drawEdge(e)
                
        for n in self.nodes:
            self.drawNode(n)
            

    
    def dfs(self):
        path = Stack.Stack()
        path.add(0)

        while path.getLength() != 0:
            pygame.time.delay(100)
            currentNode = path.getTop()
            self.nodes[currentNode].status = "visited"
            neighbors = g.allNeighborsOf[currentNode]
            random.shuffle(neighbors)

            stuck = True
            for neighborId in neighbors:
                if self.nodes[neighborId].status == "unvisited": #Node was unvisited
                    path.add(neighborId)
                    stuck = False #new node was found
                    self.edgeMatrix[currentNode][neighborId].status = "visited"
                    g.drawEdge(self.edgeMatrix[currentNode][neighborId])
                    break


            if stuck == True: #backtrack
                path.removeTop() #pop top element from Stack

            g.drawNode(self.nodes[currentNode])
            pygame.display.update()

#(nodes, edges) = GraphGenerator.fullGraph(5)
#(nodes, edges) = GraphGenerator.randomGraph(30,1)
(nodes, edges) = GraphGenerator.gridGraph(10,15)
#(nodes, edges) = GraphGenerator.sudokuGraph()

g = Graph(nodes, edges)#
print("graph nodes:", len(g.nodes), "graph edges:", len(g.edges))
g.draw()
pygame.display.update()

g.dfs()
#g.bfs() 

##    def bfs(self, currentNode):
##        currentNodes = [currentNode]
##        
##        while len(currentNodes) != 0:
##            nextNodes = []
##            g.show()
##            pygame.time.delay(5)
##
##            for node in currentNodes:
##                neighbors = g.allNeighborsOf[node]
##                for neighborId in neighbors:
##                    if self.nodes[neighborId].status == "unvisited":
##                        self.nodes[neighborId].status = "visited"
##                        nextNodes.append(neighborId)
##
##            currentNodes = deepcopy(nextNodes)



##    def dfsRecursive(self, currentNode):
##
##        g.show()
##        allNeighbors = self.allNeighborsOf[currentNode]
##        random.shuffle(allNeighbors)
##        for nodeId in allNeighbors:
##            if self.nodes[nodeId].status == "unvisited":
##                self.path.append(currentNode)
##                self.nodes[currentNode].status = "visited"
##                self.dfsRecursive(nodeId) #nextNode = currentNode
##                break
##            
##        if len(self.path) == 1:
##            return
##        
##        self.nodes[currentNode].status = "backtracked"
##        self.path = self.path[:len(self.path)-1] #remove last element from path (backtrack)
##        self.dfsRecursive(self.path[len(self.path)-1])
##        
##
## 

