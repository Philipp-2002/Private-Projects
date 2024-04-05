
import random
from copy import deepcopy
import numpy as np
import pygame
pygame.init()

screen = pygame.display.set_mode((700, 800))
f100 = pygame.font.SysFont("a", 100)
#x rüber und y runter   #es gibt 7 slots die jeweils 6 tief sind
#board[slot][tiefe]

slotOrder = [3,2,4,1,5,0,6]

def getTiefe(board, slot): #place one piece in the slot
    getY = 0

    for tiefe in range(6): #gehe von oben nach unten in den slot
        if board[slot][tiefe] is not None:  #das neue Teil stoesst auf ein anderes
            return tiefe-1
        
    return 5


def showWinner(positions): #print winning board, click for the next game
    for (slot, tiefe) in positions:
        pygame.draw.ellipse(screen, (255, 255, 255), (slot*100+10, tiefe*100+110, 80, 80),10)
    pygame.display.update()


    while True:
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                return

def showProgress(c):#show progress bar based on number of slots searched
    pygame.draw.rect(screen, (0,0,0), (300, 50, 140, 50))
    pygame.draw.rect(screen, (0,255,0), (300, 50, 20*c, 50))
    pygame.draw.rect(screen, (255,255,255), (300, 50, 140, 50),5)

    pygame.display.update()

def showBoard(board):   #show pygame board
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (150, 150, 150), (0, 100,700, 600))

    for tiefe in range(6):
        for slot in range(7):
            if board[slot][tiefe] == None:
                color = (0,0,0)
            if board[slot][tiefe] == "X":
                color = (255, 255, 0)
            if board[slot][tiefe] == "O":
                color = (255, 0, 0)
            pygame.draw.ellipse(screen, color, (slot*100+10, tiefe*100+110, 80, 80))

    pygame.display.update()
    
##    for tiefe in range(6):
##        for slot in range(7):
##            if board[slot][tiefe] == None: #translate None into - only for printing purpose
##                symbol = "-"
##            else:
##                symbol = board[slot][tiefe]
##                
##            print(symbol, end=" ") #eine Zeile des Boards printen
##        print("")


def checkWinner(board): #check if board has a winning position
    for slot in range(4): #die 3 rechtesten slots fallen weg
        for tiefe in range(6):
            if board[slot][tiefe] == "X" and board[slot+1][tiefe] == "X" and board[slot+2][tiefe] == "X" and board[slot+3][tiefe] == "X":
                return (1, [[slot,tiefe],[slot+1,tiefe],[slot+2,tiefe],[slot+3,tiefe]])
            
            if board[slot][tiefe] == "O" and board[slot+1][tiefe] == "O" and board[slot+2][tiefe] == "O" and board[slot+3][tiefe] == "O":
                return (-1, [[slot,tiefe],[slot+1,tiefe],[slot+2,tiefe],[slot+3,tiefe]])
            
    for slot in range(7):
        for tiefe in range(3,6): #die 3 obersten tiefen fallen weg
            if board[slot][tiefe] == "X" and board[slot][tiefe-1] == "X" and board[slot][tiefe-2] == "X" and board[slot][tiefe-3] == "X":
                return (1,[[slot,tiefe],[slot,tiefe-1],[slot,tiefe-2],[slot,tiefe-3]])
            
            if board[slot][tiefe] == "O" and board[slot][tiefe-1] == "O" and board[slot][tiefe-2] == "O" and board[slot][tiefe-3] == "O":
                return (-1,[[slot,tiefe],[slot,tiefe-1],[slot,tiefe-2],[slot,tiefe-3]])
            
    for slot in range(4):   #diagonalen nach rechts oben
        for tiefe in range(3,6):
            if board[slot][tiefe] == "X" and board[slot+1][tiefe-1] == "X" and board[slot+2][tiefe-2] == "X" and board[slot+3][tiefe-3] == "X":
                return (1,[[slot,tiefe], [slot+1,tiefe-1], [slot+2,tiefe-2], [slot+3,tiefe-3]])
            
            if board[slot][tiefe] == "O" and board[slot+1][tiefe-1] == "O" and board[slot+2][tiefe-2] == "O" and board[slot+3][tiefe-3] == "O":
                return (-1,[[slot,tiefe], [slot+1,tiefe-1], [slot+2,tiefe-2], [slot+3,tiefe-3]])

    for slot in range(3,7):   #diagonalen nach rechts oben
        for tiefe in range(3,6):
            if board[slot][tiefe] == "X" and board[slot-1][tiefe-1] == "X" and board[slot-2][tiefe-2] == "X" and board[slot-3][tiefe-3] == "X":
                return (1,[[slot,tiefe],[slot-1,tiefe-1],[slot-2,tiefe-2],[slot-3,tiefe-3]])
            
            if board[slot][tiefe] == "O" and board[slot-1][tiefe-1] == "O" and board[slot-2][tiefe-2] == "O" and board[slot-3][tiefe-3] == "O":
                return (-1,[[slot,tiefe],[slot-1,tiefe-1],[slot-2,tiefe-2],[slot-3,tiefe-3]])

    isFull = True
    for slot in range(7):
        if board[slot][0] is None:
            isFull = False
            break
            
    if isFull == True:
        return (0,[])

    return (None, [])
    

def makePlayerMove(board): #player makes his move
    while True:
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] > 0 and pos[0] < 700 and pos[1] > 100 and pos[1] < 600:
                    slot = int(pos[0]/100)
                    tiefe = getTiefe(board, slot)
                    board[slot][tiefe] = "O"
                    return board



def minimax(board, isMaximizing, alpha, beta, depth):
    # Generate a hash key for the current board state
    boardKey = tuple(tuple(row) for row in board)

    if isMaximizing:
        if boardKey in transpositionTableMax:
            return transpositionTableMax[boardKey]
    else:
        if boardKey in transpositionTableMin:
            return transpositionTableMin[boardKey]

    result = checkWinner(board)[0]

    if result is not None:
        return result

    if depth >= maxDepth:
        return 0

    if isMaximizing:
        bestScore = -10000000
        for slot in slotOrder:
            if board[slot][0] is None:
                tiefe = getTiefe(board, slot)
                board[slot][tiefe] = "X"
                score = minimax(board, False, alpha, beta, depth + 1)
                board[slot][tiefe] = None
                bestScore = max(bestScore, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
                
        transpositionTableMax[boardKey] = bestScore  # Store the best score in the transposition table
        return bestScore
    else:
        bestScore = 10000000
        for slot in slotOrder:
            if board[slot][0] is None:
                tiefe = getTiefe(board, slot)
                board[slot][tiefe] = "O"
                score = minimax(board, True, alpha, beta, depth + 1)
                board[slot][tiefe] = None
                bestScore = min(bestScore, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
                
        transpositionTableMin[boardKey] = bestScore  # Store the best score in the transposition table
        return bestScore

                    





def makeBestMove(board, isMaximizing): #program calculates move
    bestscore = -100000000
    
    c = 0
    for slot in slotOrder:
        if board[slot][0] is None:
            tiefe = getTiefe(board, slot)
            board[slot][tiefe] = "X" if isMaximizing else "O"
            score = minimax(board, not isMaximizing, -1000000, 1000000,0)

            board[slot][tiefe] = None #undo board move
            print("slot:" + str(slot) + "score: " + str(score))
            if score > bestscore:
                bestscore = score
                bestSlot = slot

        c += 1
        showProgress(c) #show progress bar


    tiefe = getTiefe(board, bestSlot)
    board[bestSlot][tiefe] = "X" if isMaximizing else "O"
    
    return board


transpositionTableMax = {}
transpositionTableMin = {}


while True:
    board = [[None for y in range(6)] for x in range(7)]
    showBoard(board)
    transpositionTableMax.clear()
    transpositionTableMin.clear()

    maxDepth = 10

    for iteration in range(42):
        print(" ")      
        print(len(transpositionTableMax))
        print(len(transpositionTableMin))
        if np.mod(iteration,2) == 0:
            board = makePlayerMove(board)
            showBoard(board)
        else:
            board = makeBestMove(board, True)
            showBoard(board)
            
        if checkWinner(board)[0] is not None:
            print(str(checkWinner(board)[0]) + " won") #-1 = p1 won, 0 = draw, 1 = p2 won

            showWinner(checkWinner(board)[1]) #übergebe die 4 gewinnpositionen
            break


