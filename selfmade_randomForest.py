import numpy as np
import random
from math import log
import collections
import pygame
from sklearn.datasets import make_blobs


def info(dataX, dataY):
    information = 0
    if len(dataX) != 0:
        for label in possibleLabels:
            frequency = len(dataX[dataY == label])/len(dataX) 
            if frequency != 0:
                information += frequency*log(frequency,2)
    return -information

def isPure(dataY):
    if len(dataY) == 0:
        return True

    start = dataY[0]
    for i in range(len(dataY)):
        if dataY[i] != dataY[0]:
            return False
    return True

def plotData(x,y,labels):
    for i in range(n):
        pygame.draw.ellipse(screen,(255,255,255), (x[i]-12,y[i]-12, 24, 24))
        pygame.draw.ellipse(screen,colors[labels[i]], (x[i]-10,y[i]-10, 20, 20))
    pygame.display.update()


def plotDecision(trees): #x or y, where ENCODE PREDICTION
    for attr1 in range(100):
        for attr2 in range(100):
            decisions = [0 for i in range(len(possibleLabels))]
            for tree in trees:
                predictedLabel = tree.predict(attr1*8, attr2*8)
                decisions[predictedLabel] += 1

            
            col = colors[np.argmax(decisions)] # find position with maximum count
            pygame.draw.rect(screen, col, (attr1*8, attr2*8, 8, 8))
            
    pygame.display.update()        

def attrInfo(data, labels, splitpoint):
    remainingInfo = 0
    data1 = data[data < splitpoint] #left partition
    data2 = data[data  >= splitpoint] #right partition

    labels1 = labels[data < splitpoint]
    labels2 = labels[data >= splitpoint]

    #frequency info over both splitpoint partitions
    attributeInformation = (len(data1)/n)*info(data1, labels1)+ (len(data2)/n)*info(data2, labels2)
    return attributeInformation

class DecisionTree():

    def __init__(self, x,y, labels):

        self.leftTree = None
        self.rightTree = None

        self.x = x
        self.y = y
        self.labels = labels

        self.splitpoint = None
        self.splitattribute = None

        self.isLeaf = False

    def printTree(self):
        print("x:", self.x, "\ny:", self.y, "\nlabels:", self.labels, "\nsplitpoint:", self.splitpoint, "\nsplitattribute:", self.splitattribute)

    def goLeft(self):
        return self.leftTree

    def goRight(self):
        return self.rightTree


    def split(self, attribute, splitpoint):#create leftTree and rightTree
        if attribute == "x":
            self.leftTree = DecisionTree(self.x[self.x < splitpoint],
                                                 self.y[self.x < splitpoint],
                                                 self.labels[self.x < splitpoint])
                
            self.rightTree = DecisionTree(self.x[self.x >= splitpoint],
                                             self.y[self.x >= splitpoint],
                                             self.labels[self.x >= splitpoint])
        if attribute == "y":
            self.leftTree = DecisionTree(self.x[self.y < splitpoint],
                                             self.y[self.y < splitpoint],
                                             self.labels[self.y < splitpoint])
            
            self.rightTree = DecisionTree(self.x[self.y >= splitpoint],
                                             self.y[self.y >= splitpoint],
                                             self.labels[self.y >= splitpoint])

        
    def getBestSplitpoint(self):
        splitpointsX = [(self.x[i]+self.x[i+1])/2 for i in range(len(self.x)-1)]
        splitpointsY = [(self.y[i]+self.y[i+1])/2 for i in range(len(self.y)-1)]

        infosX = [attrInfo(self.x, self.labels, splitpoint) for splitpoint in splitpointsX]
        infosY = [attrInfo(self.y, self.labels, splitpoint) for splitpoint in splitpointsY]

        
        if min(infosX) < min(infosY): #best splitting on attribute x (if equal or worse: split on y)
            self.splitattribute = "x"
            self.splitpoint = splitpointsX[np.argmin(infosX)]
        else:
            self.splitattribute = "y"
            self.splitpoint = splitpointsY[np.argmin(infosY)]
        return (self.splitattribute, self.splitpoint)

    def predict(self,x,y):
        currentTree = self
        while True:
            if currentTree.splitattribute == "x":
                if x < currentTree.splitpoint:
                    currentTree = currentTree.goLeft()
                else:
                    currentTree = currentTree.goRight()
                    
            if currentTree.splitattribute == "y":
                if y < currentTree.splitpoint:
                    currentTree = currentTree.goLeft()
                else:
                    currentTree = currentTree.goRight()
                    
            if currentTree.isLeaf == True:
                labelFrequencies = collections.Counter(currentTree.labels)
                return currentTree.labels[0] #all labels are equal MAJORITY CLASS AS PREDICTION
        


    def splitTree(self,tree):
        (splitattribute, splitpoint) = tree.getBestSplitpoint() #get info left and right
        tree.split(splitattribute, splitpoint)

        left = tree.goLeft()
        right = tree.goRight()


        if isPure(left.labels) or len(left.labels) < 5: ##left split ################10 is default
            left.isLeaf = True #do not split further
        else:
            self.splitTree(left)

        if isPure(right.labels) or len(right.labels) < 5: ##right split #######random(1,30) for random forest
            right.isLeaf = True
        else:       
            self.splitTree(right)

n = 100
possibleLabels = [0,1,2,3,4,5,6,7,8,9]



#x = np.asarray([random.randint(0,800) for i in range(n)]) #random data points
#y = np.asarray([random.randint(0,800) for i in range(n)])
#labels = np.asarray(([random.choice(possibleLabels) for i in range(n)]))

(data, labels) = make_blobs(n_samples = n,
                            n_features = len(possibleLabels),
                            centers = len(possibleLabels),
                            cluster_std = 50,
                            center_box = (100, 700))
x = (data.T)[0]
y = (data.T)[1]

#print(labels)


#print("x:", x, "\ny:", y, "\nlabels:", labels)



num_trees = 30


trees = []



for i in range(num_trees):
    indices = random.sample(list(range(n)), int((2/3)*n)) ###which fraction of initial dataset should be trained
    tree = DecisionTree(x[indices],y[indices], labels[indices])
    tree.splitTree(tree)
    trees.append(tree)



screen = pygame.display.set_mode((800, 800))
colors = [[random.randint(0,255) for c in range(3)] for i in range(len(possibleLabels))]

plotDecision(trees)
plotData(x,y, labels)





  
