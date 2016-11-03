import random

def initialize(length, width):
    return [[0 for w in range(width)] for l in range(length)]

length = 4
width = 4
num_mines = 3
board = initialize(length=length, width=width)

def get_neighbors(board, i, j):
    spots = set()
    spots.add((i, j+1))
    spots.add((i+1, j+1))
    spots.add((i+1, j))
    spots.add((i+1, j-1))
    spots.add((i, j-1))
    spots.add((i-1, j-1))
    spots.add((i-1, j))
    spots.add((i-1, j+1))
    to_remove = set()
    for spot in spots:
        if spot[0] >= len(board) or spot[0] < 0 or spot[1] >= len(board[i]) or spot[1] < 0:
            to_remove.add(spot)
    return spots - to_remove

def label_spots(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == -1:
                for (ni, nj) in list(get_neighbors(board, i,j)):
                    print ni,nj
                    if board[ni][nj] != -1:
                        board[ni][nj] += 1
    return board

def scan_forward(board, l, w):
    found = False
    while l < len(board) and not found:
        while w < len(board[l]) and not found:
            if board[l][w] != -1:
                board[l][w] = -1
                found = True      
            w += 1
        w = 0
        l += 1
    return found
        
def scan_backward(board, l, w):
    found = False
    while l >= 0 and not found:
        while w >= 0 and not found:
            if board[l][w] != -1:
                board[l][w] = -1
                found = True      
            w -= 1
        w = len(board[l])
        l -= 1

def ran_place(board, num_mines, length, width):
    num_placed = 0
    while num_placed < num_mines:
        l = random.randint(0, length-1)
        w = random.randint(0, width-1)
        if board[l][w] != -1:
            board[l][w] = -1
        else:
            found = scan_forward(board, l, w)
            if not found:
                scan_backward(board, l, w)
        num_placed += 1
    return board

board = ran_place(board, num_mines, length, width)
board = label_spots(board)
for v in board:
    print v