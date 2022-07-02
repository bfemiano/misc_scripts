import random
import pytest

def get_mines(length, width, num_mines):
    items = [i for i in range(length * width)]
    num_fetched = 0
    mines = []
    while num_fetched < num_mines:
        mine_pos = random.randint(0, len(items)-1)
        mine = items[mine_pos]
        print(items)
        print(mine_pos)
        del items[mine_pos]
        num_fetched += 1
        mine_x = int(mine / width)
        mine_y = mine % width
        mines.append((mine_x, mine_y))
    return set(mines)

    
def make_board(length, width, num_mines):
    mines = get_mines(length, width, num_mines)
    board = []
    for l in range(0, length):
        board.append([])
        for w in range(0, width):
            pos = 0
            if (l,w) in mines:
                pos = -1
            else:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (l+i, w+j) in mines:
                            pos += 1
            board[l].append(pos)
    return board

def test_runs_no_crash():
    for i in range(100): 
        make_board(length=5, width=4, num_mines=5)
    
def test_one_mine():
    board = make_board(3,3,1)
    found = 0
    for row in board:
        for column in row:
            if column == -1:
                found += 1
    assert found == 1
    
def test_found_eight_mines():
    board = make_board(3,3,8)
    found = 0
    for row in board:
        for column in row:
            if column == -1:
                found += 1
    assert found == 8
    
def test_all_around_mine_gt_zero():
    board = make_board(3,3,1)
    for l, row in enumerate(board):
        for w, column in enumerate(row):
            if column == -1:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if i == 0 and j == 0:
                            continue
                        if l+i >= 0 and w+j >= 0 and l+i < 3 and w+j < 3:
                            assert board[l+i][w+j] > 0 
    
pytest.main()

board = make_board(4,4,3)
for b in board:
    f_board = ["{c}".format(c=c) if c >= 0 else "*" for c in b]
    print(f_board)
