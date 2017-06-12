import random

def initialize(length, width):
    board = []
    available_spots = []
    for i in range(length):
        board.append([])
        for j in range(width):
            board[i].append(0)
            available_spots.append((i,j))
    return board, available_spots

length = 4
width = 4
num_mines = 7
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
                    if board[ni][nj] != -1:
                        board[ni][nj] += 1
    return board
    
def ran_place(board, available_slots, num_mines, length, width):
    num_placed = 0
    while num_placed < num_mines:
        i = random.randint(0, len(available_slots)-1)
        (l,w) = available_slots[i]
        available_slots.remove((l,w))
        board[l][w] = -1
        num_placed += 1
    return board
    
board, available_slots = initialize(length, width)
board = ran_place(board, available_slots, num_mines, length, width)
board = label_spots(board)
for v in board:
    print v