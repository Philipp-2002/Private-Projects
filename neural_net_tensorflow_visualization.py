import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import RMSprop
from copy import deepcopy
import pygame
import random
from math import sin, cos
from numpy import argmax

screen = pygame.display.set_mode((800, 800))




COLORS = 10 #anzahl farben (klassen)
PIVOTS_PER_COLOR = 1 #anzahl cluster pro farbe (klasse)
POINTS_PER_PIVOT = 30 #anzahl punkte pro punktcluster

DISTRIBUTION_POINTS_FROM_PIVOT = 15 #größe der cluster


#####hyperparameter


trainx = []
trainy = []

pivots = []
pivots = [[random.randint(0, 800) ,random.randint(0, 800)] for i in range(COLORS*PIVOTS_PER_COLOR+1)]


cols = []
cols = [[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for i in range(COLORS)]


##for i in range(POINTS_PER_PIVOT): #donut: wichtig: line 48: for c in range(1, COLORS)
##    trainx.append([(500+sin(i)*300)/1000, (500+cos(i)*400)/1000])
##    target = [0 for j in range(COLORS)]
##    target[0] = 1
##    trainy.append(target)

n = 0
for c in range(COLORS):
    for j in range(PIVOTS_PER_COLOR):
        n += 1
        streux = random.randint(1, 5)#unförmige kreise
        streuy = random.randint(1, 5)
        for i in range(POINTS_PER_PIVOT):
            trainx.append([(pivots[n][0]+streux*random.gauss(0, DISTRIBUTION_POINTS_FROM_PIVOT))/800,
                           (pivots[n][1]+streuy*random.gauss(0, DISTRIBUTION_POINTS_FROM_PIVOT))/800])

            target = [0 for j in range(COLORS)]
            target[c] = 1   #onehot
            trainy.append(target)

            
        

pixelnum = 100

visx = []
for i in range(pixelnum):
    for j in range(pixelnum):
        visx.append([i/pixelnum, j/pixelnum])






def viz():
    results = model.predict(visx, verbose = 3)
    y = 0
    x = 0
    
    for i in range(pixelnum**2):


        mclass = argmax(results[i])
        pygame.draw.rect(screen, (cols[mclass][0], cols[mclass][1], cols[mclass][2]), (x*1000/pixelnum, y*1000/pixelnum, int(1000/pixelnum), int(1000/pixelnum)))

                    
        y += 1
        if y == pixelnum:
            y = 0
            x += 1

    p = 0
    for i in range(COLORS):#iterate over all points
        for j in range(PIVOTS_PER_COLOR*POINTS_PER_PIVOT):
            pygame.draw.ellipse(screen, (0, 0, 0), (trainx[p][0]*800-6, trainx[p][1]*800-6, 12, 12))
            pygame.draw.ellipse(screen, (cols[i]), (trainx[p][0]*800-5, trainx[p][1]*800-5, 10, 10))
            p += 1
           

    pygame.display.update()


def make_model():
    model = Sequential()
    model.add(Dense(50, input_dim=2, activation='relu'))    
    model.add(Dense(50, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(COLORS, activation='sigmoid'))
    return model

model = make_model()
model.compile(loss = "categorical_crossentropy", optimizer=Adam(), metrics=['accuracy'])


running = True
while running:
    keys = pygame.event.get()
    model.fit(trainx, trainy, epochs = 1,verbose= 2, shuffle = True, batch_size = 20)
    #model.save('my_model.h5')
    viz()
    #model = models.load_model('my_model.h5')

                              
