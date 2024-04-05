from copy import deepcopy
import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((500, 500))
f100 = pygame.font.SysFont("a", 50)


cellSize = 100

def checkWinner(board):
    for i in range(3):
        if board[i][0] == "X" and board[i][1] == "X" and board[i][2] == "X":
            return 1
        if board[0][i] == "X" and board[1][i] == "X" and board[2][i] == "X":
            return 1

        if board[i][0] == "O" and board[i][1] == "O" and board[i][2] == "O":
            return -1
        if board[0][i] == "O" and board[1][i] == "O" and board[2][i] == "O":
            return -1


    if board[0][0] == "X" and board[1][1] == "X" and board[2][2] == "X":
        return 1
    if board[2][0] == "X" and board[1][1] == "X" and board[0][2] == "X":
        return 1
    
    if board[0][0] == "O" and board[1][1] == "O" and board[2][2] == "O":
        return -1
    if board[2][0] == "O" and board[1][1] == "O" and board[0][2] == "O":
        return -1        

    isFull = True
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                isFull = False
                break
    if isFull:
        return 0


def minimax(board, isMaximizing, alpha, beta):
    result = checkWinner(board)

    if result is not None: #wenn es ein finaler 
        return result

    if isMaximizing:
        bestScore = -10000000
        for x in range(3):
            for y in range(3):
                if board[x][y] is None:
                    board[x][y] = "X"
                    score = minimax(board, False, alpha, beta)
                    board[x][y] = None
                    bestScore = max(bestScore, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
                    
        return bestScore
    else:
        bestScore = 10000000
        for x in range(3):
            for y in range(3):
                if board[x][y] is None:
                    board[x][y] = "O"
                    score = minimax(board, True, alpha, beta)
                    board[x][y] = None
                    bestScore = min(bestScore, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
    
        return bestScore
                    

    
    



def makeBestMove(board,isMaximizing):
    bestscore = -100000000

        
    for x in range(3):
        for y in range(3):
            if board[x][y] is None:
                board[x][y] = "X" if isMaximizing else "O"
                score = minimax(board, not isMaximizing, -1000000, 1000000)
                board[x][y] = None
                if score > bestscore:
                    bestscore = score
                    bestmove = (x,y)

    board[bestmove[0]][bestmove[1]] = "X" if isMaximizing else "O"

    return board

def makePlayerMove(board):
    while True:
        ev = pygame.event.get()
        placed = False
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()


                if pos[0] > 100 and pos[0] < 400 and pos[1] > 100 and pos[1] < 400:

                    x = int((pos[0]-cellSize)/cellSize)
                    y = int((pos[1]-cellSize)/cellSize)

                    if board[x][y] is None:
                        board[x][y] = "O"
                        print("took move at" + str(x) + str(y))
                        placed = True
                        break
        if placed == True:
            return board

        

def showBoard(board):
    screen.fill((255, 255, 255))

    for i in range(4):
        pygame.draw.line(screen, (0,0,0), (cellSize, (i+1)*cellSize), (4*cellSize, (i+1)*cellSize),5)
        pygame.draw.line(screen, (0,0,0), ((i+1)*cellSize, cellSize), ((i+1)*cellSize, 4*cellSize),5)

    for i in range(3):
        for j in range(3):
            if board[i][j] == "X":
                pygame.draw.line(screen, (0,0,255), ((i+1)*cellSize, (j+1)*cellSize), ((i+1)*cellSize+cellSize, (j+1)*cellSize+cellSize),5)
                pygame.draw.line(screen, (0,0,255), ((i+1)*cellSize, (j+1)*cellSize+cellSize), ((i+1)*cellSize+cellSize, (j+1)*cellSize),5)
            if board[i][j] == "O":
                pygame.draw.ellipse(screen, (255, 0,0), ((i+1)*cellSize, (j+1)*cellSize, cellSize,cellSize),5)
    pygame.display.update()



def showEnd(winner):
    print(winner)

    if winner == 0:
        text = f100.render("draw", True, (100, 200, 50))
        screen.blit(text, (180, 30))

    if winner == -1:
        text = f100.render("you won ", True, (50, 200, 50))
        screen.blit(text, (180, 30))
        
    if winner == 1:
        text = f100.render("you lost", True, (200, 50, 50))
        screen.blit(text, (180, 30))


    pygame.draw.rect(screen, (0, 255, 50), (150, 420, 180, 50))
    text = f100.render("play again", True, (0,0,0))
    screen.blit(text, (150, 420))

    pygame.display.update()
    while True:
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] > 150 and pos[0] < 330:
                    if pos[1] > 420 and pos[1] < 470:
                        return 




while True:
    playerToMove = True

    board = [[None for x in range(3)] for y in range(3)]
    showBoard(board)

    for iteration in range(9):
        if playerToMove:
            board = makePlayerMove(board)
            showBoard(board)
        else:
            board = makeBestMove(board, True)#das True bedeutet, dass maximiert wird, nicht minimiert
            showBoard(board)

        if checkWinner(board) is not None:
            break
        
        playerToMove = not playerToMove
        
    showEnd(checkWinner(board))



                        
