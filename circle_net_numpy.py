from numpy import random
from numpy import exp
from numpy import zeros
from numpy import transpose
from numpy import dot
from numpy import sum
from math import dist
import pygame
screen = pygame.display.set_mode((400, 400))


iNum = 2
h1Num = 20
h2Num = 20
oNum = 1

lr = .5
#X = [[0,0], [0,1], [1,0], [1,1], [.5,.5]]
#y = [[1], [1], [1], [1], [0]]

X = []
for x in range(10):
    for y in range(10):
        X.append([x/10, y/10])
        
y = [[1 if dist(p,[.5,.5]) < .3 else 0] for p in X]


def updateWeights(nodes, weights, errors, numX,numY):
    return weights + lr*dot(transpose([nodes]), [errors])
    #for i in range(numX):
    #    for k in range(numY):
    #        weights[i][k] += lr*errors[k]*nodes[i]
    #return weights

def matmul(X,Y, sizeX, sizeY):
    return dot(X,Y)
    #nodes = zeros(sizeY)
    #for i in range(sizeX):
    #    for j in range(sizeY):
    #        nodes[j] += X[i]*Y[i][j]
    #return nodes

def activate(X):
    return 1/(1+exp(-X))

def calculateError(nodes, weights, errOut, sizeX, sizeY):
    #errOut are the error layer of the next layer
    #errors are the current errors
    #errAfter are the weighted erros of the next layer
    
    #errors = zeros(sizeX)
    #for i in range(sizeX):
    #    errAfter = 0
    #    for k in range(sizeY):
    #        errAfter += errOut[k]*weights[i][k]
    #    errors[i] = nodes[i]*(1-nodes[i])*errAfter
    #return errors
    
    return nodes*(1-nodes)*sum(dot(weights, transpose([errOut])), axis = 1)


w_ih1 = random.normal(size = (iNum, h1Num))
w_h1h2 = random.normal(size = (h1Num, h2Num))
w_h2out = random.normal(size = (h2Num, oNum))

bh1 = random.normal(size = h1Num)
bh2 = random.normal(size = h2Num)
bout = random.normal(size = oNum)


def show():
    for x in range(100):
        for y in range(100):
            inputs = [x/100, y/100]
            hidden1 = matmul(inputs, w_ih1, iNum, h1Num)+bh1  
            hidden1 = activate(hidden1)

            hidden2 = matmul(hidden1, w_h1h2, h1Num, h2Num)+bh2
            hidden2 = activate(hidden2)

            out = matmul(hidden2, w_h2out, h2Num, oNum)+bout
            out = activate(out)

            color = int(out[0]*255)

            pygame.draw.rect(screen, (color, color, color), (y*4, x*4, 4, 4))
    pygame.display.update()




iteration = 0
while True: #iteration
    iteration += 1
    for x, label in zip(X,y):
        inputs = x+random.normal(size = iNum)*.1
        target = label

        hidden1 = matmul(inputs, w_ih1, iNum, h1Num)  +bh1
        hidden1 = activate(hidden1)

        hidden2 = matmul(hidden1, w_h1h2, h1Num, h2Num) +bh2
        hidden2 = activate(hidden2)

        out = matmul(hidden2, w_h2out, h2Num, oNum) +bout
        out = activate(out)

        errorOut  = out*(1-out)*(target-out)
        errorh2 = calculateError(hidden2, w_h2out, errorOut, h2Num, oNum)
        errorh1 = calculateError(hidden1, w_h1h2, errorh2, h1Num, h2Num)


        w_h2out = updateWeights(hidden2, w_h2out, errorOut, h2Num, oNum)
        w_h1h2 = updateWeights(hidden1, w_h1h2, errorh2, h1Num, h2Num)
        w_ih1 = updateWeights(inputs, w_ih1, errorh1, iNum, h1Num)


        bh1 += lr*errorh1
        bh2 += lr*errorh2
        bout += lr*errorOut

    if iteration % 10 == 0:
        print("iteration", iteration,"input", x,"label", label, "prediction", out)



    if iteration % 10 == 0:
        show()
        print("\n")



        




