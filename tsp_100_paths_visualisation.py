import pygame
import random
import sys
from copy import deepcopy


pygame.init()

f = pygame.font.SysFont("c", 30)
fbig = pygame.font.SysFont("c", 100)

screen = pygame.display.set_mode((1000, 1000))


citnum = 30
citpos  = [[random.randint(0, 100),random.randint(0, 100)] for i in range(citnum)]

popnum = 100
pop = []


def createpaths():
    newpop = []
    for i in range(popnum):
        path = []
        path.append(0) #start city
        pathlen = 0
        
        while pathlen < citnum-1:
            test = random.randint(0, citnum-1)
            if test not in path:
                pathlen += 1
                path.append(test)
        path.append(0) #end city
        newpop.append(path)
    return newpop


def vizmany():
    screen.fill(0)
    x = 0
    y = 0
    for i in range(popnum):
        if x == 1000:
            x = 0
            y += 100

        pygame.draw.rect(screen, (255, 255, 255), (x, y, 100, 100), 1)#draw bounderies
        for j in range(citnum):
            pygame.draw.rect(screen, (255, 255, 0), (x+citpos[pop[i][j]][0]-2, y+citpos[pop[i][j]][1]-2, 4, 4)) #draw cities
            pygame.draw.line(screen, (255, 255, 255), (x+citpos[pop[i][j]][0], y+citpos[pop[i][j]][1]), (x+citpos[pop[i][j+1]][0], y+citpos[pop[i][j+1]][1]))#draw paths

        pygame.draw.line(screen, (200, 100, 255), (x+citpos[pop[i][j]][0], y+citpos[pop[i][j]][1]), (x+citpos[pop[i][0]][0], y+citpos[pop[i][0]][1]))#draw last line
        screen.blit(f.render(str(i), True,(255, 255, 255)), (x+1, y+1))
        
        #screen.blit(f.render(str(int(fitnesses[i]*100000000)),True,(255, 255, 255)), (x+50, y)) #blit fitnesses

        x += 100

    pygame.display.update()

def vizbest(p):
    screen.fill(0)
    for j in range(citnum):
        pygame.draw.rect(screen, (255, 255, 0), (citpos[p[j]][0]*10-10, citpos[p[j]][1]*10-10, 20, 20)) #draw cities
        pygame.draw.line(screen, (255, 255, 255), (citpos[p[j]][0]*10, citpos[p[j]][1]*10), (citpos[p[j+1]][0]*10, citpos[p[j+1]][1]*10))#draw best path
        
    pygame.draw.line(screen, (255, 255, 255), (citpos[p[j]][0]*10, citpos[p[j]][1]*10), (citpos[p[0]][0]*10, citpos[p[0]][1]*10))#draw last line
    
    screen.blit(fbig.render(("weglänge:"+str(int(distances[popnum-1]*10))), True,(255, 255, 255)), (0, 0)) #blit end text
    pygame.display.update()
    




def calculatedistances():
    d = [0 for i in range(popnum)]
    for i in range(popnum):
        for j in range(citnum):
            d[i] += ((citpos[pop[i][j]][0]-citpos[pop[i][j+1]][0])**2+(citpos[pop[i][j]][1]-citpos[pop[i][j+1]][1])**2)**.5 #sum up all distances
        #d[i] += ((citpos[pop[i][j]][0]-citpos[pop[i][0]][0])**2+(citpos[pop[i][j]][1]-citpos[pop[i][0]][1])**2)**.5 #add start end line
        
    return d
    

def calculatefitnesses():
    f = [0 for i in range(popnum)]

    for i in range(popnum):
        f[i] = 1/distances[i]**30

##    avgdist = sum(distances)/popnum
##
##    highestdif = 0
##    for i in range(popnum):
##        if (distances[i]-avgdist) < highestdif:
##            highestdif = distances[i]-avgdist
##
##    
##    for i in range(popnum):
##        f[i] = 1/(distances[i]-avgdist+abs(highestdif)+100)**5
    
    return f


def calculatefitnessstack():
    fstack = [0 for i in range(popnum)]
    s = 0
    factor = 1/sum(fitnesses)
    
    for i in range(popnum):
        s += fitnesses[i]*factor
        fstack[i] = s
    return fstack
    

def selection():
    parentp = [0 for i in range(popnum)]
    
    for i in range(popnum-1):#elitism
        rnum = random.uniform(0, 1)
        for j in range(popnum):
            if fitnessstack[j] > rnum:
                parentp[i] = deepcopy(pop[j]) #parent pop is completely separated from initial population
                break


    bestpath = [] #elitism
    highestfitness = 0
    for i in range(popnum):
        if fitnesses[i] > highestfitness:
            highestfitness = fitnesses[i]
            bestpath = pop[i]
            
    parentp[popnum-1] = bestpath# [...,...,...,elitepath]

            
    return parentp




def crossover(parentpop):
    for i in range(20): #how many paths should crossover
        crop = random.randint(1, citnum-1)

        for j in range(crop):
            childpath1 = parentpop[2*j][:crop]
            childpath2 = parentpop[2*j+1][:crop]
              

        for j in parentpop[2*j+1]:
            if j not in childpath1:
                childpath1.append(j)

        for j in parentpop[2*j]:
            if j not in childpath2:
                childpath2.append(j)

        childpath1.append(0)
        childpath2.append(0)


        parentpop[2*i] = childpath1
        parentpop[2*i+1] = childpath2

        
    return parentpop


def swapmutation(mpop):
    swaprate = 2
    for i in range(popnum-1):
        for j in range(citnum): #randomly swap two cities
            if random.randint(0, 100) < swaprate:
                spot1 = random.randint(1, citnum-1)
                spot2 = random.randint(1, citnum-1)
                temp = deepcopy(mpop[i][spot2])
                mpop[i][spot2] = deepcopy(mpop[i][spot1])
                mpop[i][spot1] = temp
    return mpop


def chunkreversemutation(mpop):
    for i in range(popnum-1):
        for g in range(5):
            if random.randint(0, 100) < 10:
                c1 = random.randint(1, citnum-1)
                c2 = random.randint(1, citnum-1)
                
                if c1 != c2:
                    chunk = mpop[i][c1:c2]
                    chunk.reverse()
                    

                for j in range(c1, c2):
                    mpop[i][j] = chunk[j-c1]
    return mpop


def chunkreplacemutation(mpop):
    for i in range(popnum-1):
        for g in range(5):
            if random.randint(0, 100) < 10:
                chunklen = random.randint(2, 5)
                c1 = random.randint(1, citnum-chunklen-1) # oder citnum-cutlen
                c2 = c1+chunklen

                chunk = deepcopy(mpop[i][c1:c2]) #crop chunk out

                for j in chunk:
                    mpop[i].remove(j) #remove chunk from path


                insertpos = random.randint(1, citnum-chunklen-2) #select insertion pos for chunk

                newpath = []
                for j in range(insertpos):
                    newpath.append(mpop[i][j]) #append path before chunk

                for j in range(chunklen):
                    newpath.append(chunk[j]) #append chunk
                    
                for j in range(insertpos, citnum-chunklen+1): #append path after chunk
                    newpath.append(mpop[i][j])
                    
                mpop[i] = newpath
                #print(mpop[i])

    return mpop

        
        

pop = createpaths()

for g in range(400):
    calculatedistances()
    distances = calculatedistances() #create distances array
    fitnesses = calculatefitnesses()
    fitnessstack = calculatefitnessstack()
    parentpop = selection()
    #pop = crossover(parentpop)
    pop = parentpop #!!!!!!!!bei crossover raus nehmen
    pop = swapmutation(pop)
    pop = chunkreversemutation(pop)
    pop = chunkreplacemutation(pop)


    vizmany()
vizbest(pop[popnum-1])
    

