import numpy as np
import random 
import copy
from functools import lru_cache


board = np.full((3, 3), " ")


for i in range (3):
    for j in range(3):
        board[i][j]="."

board[2][2] = "o"
board[1][2] = "o"
board[0][0] = "P"
current_row = 0
current_col = 0
score=0

def find_pacman(board):
    for i in range(3):
        for j in range(3):
            if board[i][j]=="P":
                position=(i, j)
                return position
        
def fake_move(board, move, current_row,current_col):
    global score
    board_copy=copy.deepcopy(board)
    row, col = move
    if board_copy[row][col] == '.':  # Check if the move is valid
        board_copy[current_row][current_col]=" "
        board_copy[row][col] = 'P'
        current_row=row
        current_col=col
        for row in board_copy:
            print(' '.join(row))
        return board_copy 
    
    if board_copy[row][col] == ' ':
        board_copy[current_row][current_col]=" "
        board_copy[row][col] = 'P'  # Assuming 'X' represents the player's move
        fake_c_r=row
        fake_c_c=col
        for row in board_copy:
            print(' '.join(row))
        return board_copy  # Move successfully made

def make_move(board, move, current_row,current_col):
    global score
    row, col = move
    if board[row][col] == '.':  # Check if the move is valid
        board[current_row][current_col]=" "
        score+=9
        board[row][col] = 'P'
        current_row=row
        current_col=col
        evaluate()
        for row in board:
            print(' '.join(row))
        return board
    
    if board[row][col] == ' ':
        board[current_row][current_col]=" "
        score-=1
        board[row][col] = 'P'  # Assuming 'X' represents the player's move
        current_row=row
        current_col=col
        evaluate()
        for row in board:
            print(' '.join(row))
        return board  # Move successfully made


def evaluate():
    print(score)
    return 1

def game_over():
    # Check rows
    return 0

def get_possible_moves(board, current_row,current_col):
    
    possible_moves = []
    if current_row - 1 >=0:
        if board[current_row - 1 ,current_col] != 'o' and board[current_row - 1,current_col] != 'G':
            possible_moves.append((current_row -1, current_col))

    if current_row + 1 <3:
        if board[current_row  ,current_col] != 'o' and board[current_row ,current_col] != 'G':
            possible_moves.append((current_row +1, current_col))

    if current_col - 1 >=0:
        if board[current_row][current_col - 1] != 'o' and board[current_row - 1][current_col] != 'G':
            possible_moves.append((current_row , current_col -1))
    if current_col + 1 <3:#################################################
        if board[current_row ][current_col +1] != 'o' and board[current_row - 1][current_col] != 'G':
            possible_moves.append((current_row, current_col +1))
    for row in possible_moves:
        print(row)
    return possible_moves


def get_best_move(board, depth,current_row,current_col):
    best_eval = float('-inf')
    best_move = None
    board_copy=copy.deepcopy(board)
    for move in get_possible_moves(board_copy, current_row,current_col):
        new_board = fake_move(board_copy, move, current_row,current_col)
        #for row in new_board:
        #    print(' '.join(row))
        r,c=move
        eval = minimax(new_board, depth - 1, False)
        if eval > best_eval:
            best_eval = eval
            best_move = move
    make_move(board, best_move, current_row,current_col)
    return best_move
@lru_cache
def minimax(board, depth, maximizing_player):
    
    # Base case: check if the game has ended or maximum depth has been reached
    loc=find_pacman(board)
    for row in board:
            print(' '.join(row))

    if depth == 0 or game_over()==1:
        return evaluate()
    board_copy=copy.deepcopy(board)
    max_eval = float('-inf')
    min_eval = float('inf')
    if maximizing_player:
        for move in get_possible_moves(board_copy, loc[0],loc[1]):
            new_board = fake_move(board_copy, move,  loc[0],loc[1])
            eval = minimax(new_board, depth - 1, False)
            max_eval = max(max_eval, eval)
        for row in board:
            print(' '.join(row))
        return max_eval
    else:
        for move in get_possible_moves(board_copy,loc[0],loc[1]):
            new_board = fake_move(board_copy, move,  loc[0],loc[1])
            eval = minimax(new_board, depth - 1, True)
            min_eval = min(min_eval, eval)
        for row in board:
            print(' '.join(row))
        return min_eval




for row in board:
    print(' '.join(row))
#get_possible_moves(board, current_row, current_col)

#for i in range(3):
##
get_best_move(board, 1,current_row,current_col)
#print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#for row in board:
#    print(' '.join(row))
#print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#loc=find_pacman(board)
##print(loc)
#get_best_move(board, 1,loc[0],loc[1])
#print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#for row in board:
#    print(' '.join(row))
#print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#loc=find_pacman(board)
#get_best_move(board, 1,loc[0],loc[1])
#print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#for row in board:
#    print(' '.join(row))
#print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
for row in board:
    print(' '.join(row))