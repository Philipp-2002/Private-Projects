from numpy import random
from numpy import exp
from numpy import zeros
from numpy import transpose
from numpy import dot
from numpy import sum
from numpy import argmax
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split


def toOneHot(Y, numClasses):
    oneHotY = []
    for i in range(len(Y)):
        newY = [0 for k in range(numClasses)]
        newY[Y[i]] = 1
        oneHotY.append(newY)
    return oneHotY

data = load_digits()
(trainX, testX, trainY, testY)  = train_test_split(data['data'], data['target'], test_size=.25, random_state=0)

trainX = trainX/16 -.5
testX = testX/16 - .5

trainY = toOneHot(trainY, 10)
testY = toOneHot(testY,10)


X = trainX
y = trainY

iNum = 64
h1Num = 30
h2Num = 30
oNum = 10

lr = .05

print("number of train data:", len(X))
print("size of train data:", len(X[0]))


def updateWeights(nodes, weights, errors, numX,numY):
    return weights + lr*dot(transpose([nodes]), [errors])

def matmul(X,Y, sizeX, sizeY):
    return dot(X,Y)

def activate(X):
    return 1/(1+exp(-X))

def calculateError(nodes, weights, errOut, sizeX, sizeY):  
    return nodes*(1-nodes)*sum(dot(weights, transpose([errOut])), axis = 1)

def predict(inputs):
    hidden1 = matmul(inputs, w_ih1, iNum, h1Num)  
    hidden1 = activate(hidden1)

    hidden2 = matmul(hidden1, w_h1h2, h1Num, h2Num)
    hidden2 = activate(hidden2)

    out = matmul(hidden2, w_h2out, h2Num, oNum)
    out = activate(out)
    return out


def score(X,Y):
    correct = 0
    for inputs, target in zip(X,Y):
        results = predict(inputs)

        if argmax(results) == argmax(target):
            correct += 1
            
    return correct/len(X)

w_ih1 = random.normal(size = (iNum, h1Num))
w_h1h2 = random.normal(size = (h1Num, h2Num))
w_h2out = random.normal(size = (h2Num, oNum))


iteration = 0
for iteration in range(50): #iteration
    for x, label in zip(X,y):
        inputs = x+random.normal(size = iNum)*.05
        target = label

        hidden1 = matmul(inputs, w_ih1, iNum, h1Num)  
        hidden1 = activate(hidden1)

        hidden2 = matmul(hidden1, w_h1h2, h1Num, h2Num)
        hidden2 = activate(hidden2)

        out = matmul(hidden2, w_h2out, h2Num, oNum)
        out = activate(out)

        errorOut  = out*(1-out)*(target-out)
        errorh2 = calculateError(hidden2, w_h2out, errorOut, h2Num, oNum)
        errorh1 = calculateError(hidden1, w_h1h2, errorh2, h1Num, h2Num)


        w_h2out = updateWeights(hidden2, w_h2out, errorOut, h2Num, oNum)
        w_h1h2 = updateWeights(hidden1, w_h1h2, errorh2, h1Num, h2Num)
        w_ih1 = updateWeights(inputs, w_ih1, errorh1, iNum, h1Num)



    if iteration % 10 == 0:
        print("iteration", iteration, "testAccracy", score(testX, testY))
        print("iteration", iteration, "trainAccuracy", score(trainX, trainY))

    iteration += 1

print("training finished")

import pygame
pygame.init()

f50 = pygame.font.SysFont("c", 50)
screen = pygame.display.set_mode((800, 800))
screen.fill((255, 255, 255))
pygame.display.update()

grid = zeros(shape = (8,8))


def showGrid():
    for i in range(8):
        for j in range(8):
            c = 255-grid[i][j]*255 #opposite of value
            pygame.draw.rect(screen, (c, c, c), (100*j, 100*i, 100, 100))

def updateGrid():
    pygame.event.get()
    if pygame.mouse.get_pressed()[0]:
        mousepos = pygame.mouse.get_pos()
        if mousepos[0] > 0 and mousepos[0] < 800:
            if mousepos[1] > 0 and mousepos[1] < 800:
                y = int(mousepos[0]/100)
                x = int(mousepos[1]/100)
                grid[x][y] = min(1, grid[x][y] +.3)
                showGrid()
                showPrediction()
                pygame.display.update()
                pygame.time.delay(50)

def showPrediction():
    results = predict(grid.flatten())
    for i in range(10):
        screen.blit(f50.render(str(i),True,  (0)), (10, i*80))
        pygame.draw.rect(screen, (0, 0, 255), (50, i*80, 100, 30))
        pygame.draw.rect(screen, (0, 255, 0), (50, i*80, int(100*results[i]), 30))

    highestclass = argmax(results)
    pygame.draw.rect(screen, (0, 255, 0), (50, highestclass*80, 50, 30), 3)


showGrid()
showPrediction()
screen.blit(f50.render("draw a digit",True,  (0)), (250, 250))
pygame.display.update()
while True:
    updateGrid()
                



                
