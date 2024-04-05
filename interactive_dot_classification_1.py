import pygame
import random
from copy import deepcopy
import math
import numpy as np



pygame.init()
f50 = pygame.font.SysFont("c", 50)
f40 = pygame.font.SysFont("c", 40)

screen = pygame.display.set_mode((1500, 1000))

trainx = []
trainy = []

class Points: #Data
    def __init__(self):
         self.points = [[] for i in range(8)] #space for every class
         self.pointnum = 0

         
    def createpoint(self, x, y, classindex):
        self.points[classindex].append([x, y])
        
        trainx.append([x/500, y/500])
        
        label = [0 for i in range(8)] #OHE with 8 colors
        label[classindex] = 1
        trainy.append(label)
        self.pointnum += 1


    def show(self):

        pygame.draw.rect(screen, (100, 100, 100), (0, 500, 700, 500), 5)
        pygame.draw.rect(screen, (100, 100, 100), (0, 0, 700, 500), 5)
        
        for i in range(8):
            for j in self.points[i]:
                pygame.draw.ellipse(screen, (100, 100, 100), (j[0]-14, j[1]-14, 28, 28))
                pygame.draw.ellipse(screen, (env.palette[i][4:]), (j[0]-12, j[1]-12, 24, 24))
                
         
 


class Env: #Buttons

    def __init__(self):
        self.palette = np.asarray([(500, 0, 100, 100, 255, 255, 255),#"white": 
                        (500, 100, 100, 100, 255, 255, 0),#"yellow": 
                        (500, 200, 100, 100, 255, 0, 0),#"red": 
                        (500, 300, 100, 100, 255, 0, 255),#"lila": 
                        (600, 0, 100, 100, 0, 0, 255),#"blue": 
                        (600, 100, 100, 100, 0, 255, 255),#"cyan": 
                        (600, 200, 100, 100, 0, 255, 0),#green":
                        (600, 300, 100, 100, 0, 0, 0)])#"black":
        

        self.selectedcolorindex = 0
        self.pointnum = 0   #iterator

        self.drawing = True



    def mouseonbutton(self, index):
        if mousepos[0] > self.palette[index][0]:
            if mousepos[1] > self.palette[index][1]:
                if mousepos[0] < self.palette[index][0]+self.palette[index][2]:
                    if mousepos[1] < self.palette[index][1]+self.palette[index][3]:
                        return True



    def show(self):
        for i in range(8):
            pygame.draw.rect(screen, (env.palette[i][4:]), self.palette[i][:4])

            #screen.blit(f20.render((key),True, (0, 0,0)), (self.colors[key][0], self.colors[key][1]) )           

        pygame.draw.rect(screen, (100, 100, 100), (self.palette[self.selectedcolorindex][:4]), 3)

        pygame.draw.rect(screen, (0, 255, 0), (500, 400, 100, 100)) #"start training" button

        
        screen.blit(f50.render(("train"),True, (100, 100,0)), (510,440))           

                

    def update(self):
        if leftmousepressed:
            if mousepos[0] > 500:
                for i in range(8):#["white", "yellow","red","lila","blue","cyan","green","black"]
                    if self.mouseonbutton(i):
                        self.selectedcolorindex = i

                if mousepos[1] > 400: #drawing finished
                    self.drawing= False
                    
                    print("drawing finished")
                
            else:
                points.createpoint(mousepos[0], mousepos[1], self.selectedcolorindex)
                self.pointnum += 1
                pygame.time.delay(100) # time between the next dot




            
class NN:
    def __init__(self):

        self.inputnum = 2
        self.hiddennum = 10
        self.outputnum = 8

        self.lr = .05

        self.wih = np.asarray([[random.gauss(0,1) for i in range(self.inputnum )] for j in range(self.hiddennum)])
        self.who = np.asarray([[random.gauss(0,1) for i in range(self.hiddennum)] for j in range(self.outputnum)])
        
        self.cellnum = 25 #compartments with weighted probabs
        self.cellsize = int(500/self.cellnum)

        self.pixelnum = 4 #pixels per field
        self.pixelsize = int(self.cellsize/self.pixelnum)


        self.errorhistory = []
        self.accuracyhistory = []

        self.vizx = []
        for i in range(self.cellnum):
            for j in range(self.cellnum):
                self.vizx.append([i/self.cellnum, j/self.cellnum])

    def actfunc(self,x):
        act = 1/(1+np.exp(-x))
        return act

    
    
    def predict(self,inputs):
        hiddenin = np.dot(self.wih, inputs)
        hiddenout = self.actfunc(hiddenin)

        outputin = np.dot(self.who, hiddenout)
        outputout = self.actfunc(outputin)

        return outputout

    def train(self):
        rightcounter = 0
        falsecounter = 0


        xlist = list(range(0,points.pointnum))
        random.shuffle(xlist)
        #outputerrors = np.array([0.0 for i in range(8)], ndmin = 2).T
        meansquareerror = 0
        for t in xlist:########über wie viele samples soll trainiert werden

            inputs = np.array(trainx[t], ndmin = 2).T
            target = np.array(trainy[t], ndmin = 2).T

            hiddenin = np.dot(self.wih, inputs)
            hiddenout = self.actfunc(hiddenin)

            outputin = np.dot(self.who, hiddenout)
            outputs = self.actfunc(outputin)


            if np.argmax(target) == np.argmax(outputs):
                rightcounter += 1
            else:
                falsecounter += 1

            outputerrors = target-outputs
            meansquareerror += sum(outputerrors**2)

            hiddenerrors = np.dot(np.transpose(self.who),outputerrors)
            self.who += self.lr*np.dot((outputerrors*outputs*(1-outputs)),np.transpose(hiddenout))
            self.wih += self.lr*np.dot((hiddenerrors*hiddenout*(1-hiddenout)),np.transpose(inputs))

        if epochs > 0:
            self.errorhistory.append(float(meansquareerror))
            self.accuracyhistory.append(max(.001,rightcounter/points.pointnum))
        #print("accuracy:", rightcounter/points.pointnum, "error_mse", sum(outputerrors**2))
        
    def showpredictions(self):
        population = list(range(0, 8)) #all classnumbers in list

        for xpiv in range(self.cellnum):
            for ypiv in range(self.cellnum):
                predictionvector = self.predict([xpiv/self.cellnum, ypiv/self.cellnum])
                pygame.draw.rect(screen,(env.palette[np.argmax(predictionvector)][4:]), (xpiv*self.cellsize,ypiv*self.cellsize, self.cellsize, self.cellsize))
                
                #pixelgrid = np.asarray(random.choices(population,weights=predictionvector**2, k=self.pixelnum*self.pixelnum)) #get weighted array
                #pixelgrid = pixelgrid.reshape(self.pixelnum, self.pixelnum)

                #for x in range(self.pixelnum):
                #    for y in range(self.pixelnum):
                #        pygame.draw.rect(screen, (env.palette[pixelgrid[x][y]][4:]), (xpiv*self.cellsize+x*self.pixelsize, ypiv*self.cellsize+y*self.pixelsize, self.pixelsize, self.pixelsize))
                        
        
    def showgraph(self):
        pygame.draw.rect(screen,(0),(0, 500, 700, 500))
        le = len(self.errorhistory)

        if le >= 2:
            yerrorfactor = 480/max(self.errorhistory)
            yaccuracyfactor = 480
            
            xlist = [(500/le)*i for i in range(le)]

            for i in range(le-1):
                pygame.draw.line(screen, (255, 0, 0), (xlist[i]+100, 990-self.errorhistory[i]*yerrorfactor), (xlist[i+1]+100, 990-self.errorhistory[i+1]*yerrorfactor))
                pygame.draw.line(screen, (0, 255, 0), (xlist[i]+100, 990-self.accuracyhistory[i]*yaccuracyfactor), (xlist[i+1]+100,990-self.accuracyhistory[i+1]*yaccuracyfactor))


            for t in range(10):
                screen.blit(f40.render((str(np.float16((t/10)*max(self.errorhistory)))),True, (255, 0,0)), (10,990-t*50))           
                screen.blit(f40.render((str(np.float16(t/10))),True, (0, 255,0)), (610,990-t*50))           
   
             #screen.blit(f50.render(("train"),True, (100, 100,0)), (510,440))           


class Graphicnet:

    def __init__(self):
        self.inputpos = [[800, 500+i*(500/nn.inputnum)+(500/nn.inputnum)/2] for i in range(nn.inputnum)]
        self.hiddenpos = [[1100, 500+i*(500/nn.hiddennum)+(500/nn.hiddennum)/2] for i in range(nn.hiddennum)]        
        self.ouputpos = [[1400, 500+i*(500/nn.outputnum)+(500/nn.outputnum)/2] for i in range(nn.outputnum)]

    def show(self):

        for i in range(nn.inputnum):
            pygame.draw.ellipse(screen, (255, 255, 255), (self.inputpos[i][0]-5, self.inputpos[i][1]-5, 10, 10))

        for i in range(nn.hiddennum):
            pygame.draw.ellipse(screen, (255, 255, 255), (self.hiddenpos[i][0]-5, self.hiddenpos[i][1]-5, 10, 10))
            
        for i in range(nn.outputnum):
            pygame.draw.ellipse(screen, (255, 255, 255), (self.ouputpos[i][0]-5, self.ouputpos[i][1]-5, 10, 10))

            
                                
        for i in range(nn.inputnum):
            for j in range(nn.hiddennum):
                if abs(nn.wih[j][i]) > 1:
                    if nn.wih[j][i] < 0:
                        color = (255, 0, 0)
                    else:
                        color = (0, 255, 0)
                else:
                    color = (100, 100, 100)
                    
                pygame.draw.line(screen, color, self.inputpos[i], self.hiddenpos[j], 2)
                


        for i in range(nn.hiddennum):
            for j in range(nn.outputnum):
                if abs(nn.who[j][i]) > 1:
                    if nn.who[j][i] < 0:
                        color = (255, 0, 0)
                    else:
                        color = (0, 255, 0)
                else:
                    color = (100, 100, 100)
                
                pygame.draw.line(screen, color, self.hiddenpos[i], self.ouputpos[j], 2)
            

    
env = Env()
points = Points()
nn = NN()
graphicnet = Graphicnet()



while env.drawing == True:
    screen.fill(0)
    pygame.event.get()

    leftmousepressed = pygame.mouse.get_pressed()[0]
    rightmousepressed = pygame.mouse.get_pressed()[2]
    
    mousepos = pygame.mouse.get_pos()
    
    env.update() #update pointdrawing
    
    points.show()
    env.show()
    graphicnet.show()

    pygame.display.update()





training = True

epochs = 0
while training:
    if points.pointnum != 0:
        nn.train()#int(env.pointnum/8))
        
        nn.showpredictions()
        nn.showgraph()
        graphicnet.show()
        points.show()
        

        pygame.display.update()

    epochs += 1







    
