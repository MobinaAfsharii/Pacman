
import numpy as np
import random 
import copy


g1_score=0
g2_score=0
score=0

board = np.full((11, 20), ".")

for i in range (11):
    board[i,0]="o"
    board[i,19]="o"
for i in range(20):
    board[0,i]="o"
    board[10,i]="o"
# add walls
board[2,2]=board[3,2]=board[4,2]=board[6,2]=board[7,2]=board[8,2]="o"
board[2,17]=board[3,17]=board[4,17]=board[6,17]=board[7,17]=board[8,17]="o"
board[2,3]=board[8,3]= "o"
board[2,16]=board[8,16]= "o"
board[4,4]=board[4,5]="o"
board[6,4]=board[6,5]="o"
board[4,14]=board[4,15]="o"
board[6,14]=board[6,15]="o"
board[1,5]=board[2,5]=board[8,5]=board[9,5]="o"
board[1,14]=board[2,14]=board[8,14]=board[9,14]="o"
board[8,7]=board[8,8]=board[8,9]=board[8,10]=board[8,11]=board[8,12]="o"
board[6,7]=board[6,8]=board[6,9]=board[6,10]=board[6,11]=board[6,12]="o"
board[2,7]=board[2,8]=board[2,9]=board[2,10]=board[2,11]=board[2,12]="o"
board[5,7]=board[4,7]=board[5,12]=board[4,12]=board[4,8]=board[4,11]="o"

class Ghost:
    def __init__(self,ghost_row,ghost_col) -> None:
        self.ghost_row=ghost_row
        self.ghost_col=ghost_col
        board[ghost_row][ghost_col]='G'
        self.last_pos="."
    
    def move(self):

        rand=random.randint(1,4)
        changed=0
        if rand == 1:
            if board[self.ghost_row - 1][self.ghost_col] != 'o' and board[self.ghost_row - 1][self.ghost_col] != 'G':
                if board[self.ghost_row - 1][self.ghost_col] == 'o':
                    changed=1
                board[self.ghost_row][self.ghost_col] = self.last_pos  # Clear the current position
                self.ghost_row -= 1  # Move up
                self.last_pos=board[self.ghost_row][self.ghost_col] 
                board[self.ghost_row][self.ghost_col] = 'G'  # Update the new position
                changed=1
        if rand == 2:
            if board[self.ghost_row ][self.ghost_col + 1] != 'o' and board[self.ghost_row ][self.ghost_col + 1] != 'G':
                if board[self.ghost_row ][self.ghost_col +1] == 'o':
                    changed=1
                board[self.ghost_row][self.ghost_col] = self.last_pos   # Clear the current position
                self.ghost_col += 1  # Move right
                self.last_pos=board[self.ghost_row][self.ghost_col]
                board[self.ghost_row][self.ghost_col] = 'G'  # Update the new position
                changed=1
        if rand == 3:
            if board[self.ghost_row + 1][self.ghost_col] != 'o' and board[self.ghost_row + 1][self.ghost_col] != 'G':
                if board[self.ghost_row + 1][self.ghost_col] == 'o':
                    changed=1
                board[self.ghost_row][self.ghost_col] = self.last_pos   # Clear the current position
                self.ghost_row += 1  # Move up
                self.last_pos=board[self.ghost_row][self.ghost_col]
                board[self.ghost_row][self.ghost_col] = 'G'  # Update the new position
                changed=1
        if rand == 4:
            if board[self.ghost_row ][self.ghost_col - 1] != 'o' and board[self.ghost_row ][self.ghost_col - 1] != 'G':
                if board[self.ghost_row][self.ghost_col -1] == 'o':
                    changed=1
                board[self.ghost_row][self.ghost_col] = self.last_pos   # Clear the current position
                self.ghost_col -= 1  # Move up
                self.last_pos=board[self.ghost_row][self.ghost_col]
                board[self.ghost_row][self.ghost_col] = 'G'  # Update the new position
                changed=1

def find_ghost(board):
    position=[]
    for i in range(11):
        for j in range(20):
            if board[i][j]=="G":
                position.append([i, j])
    return position

def find_pacman(board):
    position=0
    for i in range(11):
        for j in range(20):
            if board[i][j]=='P':
                position=[i, j]
                return position

def distance(board,ghost_loc):
    p=find_pacman(board)
    dist1=abs(ghost_loc[0]-p[0])+abs(ghost_loc[1]-p[1])-1
    
    return dist1
         
def ghost_possible_move(board,id):
    possible_moves = []
    current_row,current_col=find_ghost(board)[0]
    if current_row - 1 >=0:
        if (board[current_row - 1 ][current_col] != 'o' and board[current_row - 1][current_col] != 'G') or board[current_row -1][current_col ]=='P':
            possible_moves.append([current_row -1, current_col])

    if current_row + 1 <11:
        if (board[current_row +1 ][current_col] != 'o' and board[current_row +1][current_col] != 'G') or board[current_row +1][current_col ]=='P':
            possible_moves.append([current_row +1, current_col])

    if current_col - 1 >=0:
        if (board[current_row][current_col - 1] != 'o' and board[current_row ][current_col-1] != 'G') or board[current_row ][current_col -1]=='P':
            possible_moves.append([current_row , current_col -1])

    if current_col + 1 <20:
        if (board[current_row ][current_col +1] != 'o' and board[current_row ][current_col+1] != 'G') or board[current_row ][current_col +1]=='P':
            possible_moves.append([current_row, current_col +1])

    if  board[current_row +1  ][current_col] == 'o' or board[current_row -1  ][current_col]=="o" or board[current_row  ][current_col+1]=="o" or board[current_row   ][current_col -1]=="o":
        possible_moves.append([current_row, current_col])
        
    if  board[current_row +1 ][current_col] == 'G' or board[current_row -1 ][current_col]=="G" or board[current_row ][current_col+1]=="G" or board[current_row ][current_col -1]=="G":
        possible_moves.append([current_row, current_col])
        
    return possible_moves

def pacman_possible_moves(board, current_row,current_col):
    
    possible_moves = []
    if current_row - 1 >=0:
        if board[current_row - 1 ,current_col] != 'o' and board[current_row - 1,current_col] != 'G':
            possible_moves.append([current_row -1, current_col])

    if current_row + 1 <11:
        if board[current_row +1 ,current_col] != 'o' and board[current_row +1,current_col] != 'G':
            possible_moves.append([current_row +1, current_col])

    if current_col - 1 >=0:
        if board[current_row][current_col - 1] != 'o' and board[current_row ][current_col-1] != 'G':
            possible_moves.append([current_row , current_col -1])
    if current_col + 1 <20:
        if board[current_row ][current_col +1] != 'o' and board[current_row ][current_col+1] != 'G':
            possible_moves.append([current_row, current_col +1])

    if  board[current_row +1  ,current_col] == 'o' or board[current_row -1  ,current_col]=="o" or board[current_row  ,current_col+1]=="o" or board[current_row   ,current_col -1]=="o":
        possible_moves.append([current_row, current_col])

    return possible_moves

def ghost1_fake_move(board, move, current_row,current_col):
    global g1_score
    board_copy=copy.deepcopy(board)
    [row, col] = move
    print(type(board_copy))

    if board_copy[row][col]=="P":
        board_copy[current_row][current_col] = " "
        board_copy[row][col] = 'G'
        g1_score+=1000
        evaluate_g1()
        g1_score-=1000
        for row in board_copy:
            print(' '.join(row))
        return board_copy

    elif distance(board_copy, move)<distance(board_copy, (current_row,current_col)):
        board_copy[current_row][current_col] = " "
        board_copy[row][col] = 'G'
        g1_score+=1
        evaluate_g1()
        g1_score-=1
        for row in board_copy:
            print(' '.join(row))
        return board_copy 
    
    elif distance(board_copy, [current_row,current_col])==distance(board_copy, move):
        evaluate_g1()
        for row in board_copy:
            print(' '.join(row))
        return board_copy 
    elif distance(board_copy, [current_row,current_col])<distance(board_copy, move):
        board_copy[current_row][current_col]=" "
        board_copy[row][col] = 'G'
        g1_score-=1
        evaluate_g1()
        g1_score+=1
        for row in board_copy:
            print(' '.join(row))
        return board_copy 
    elif (row==current_row) and (col==current_col):
        evaluate_g1()
        for row in board_copy:
            print(' '.join(row))
        return board_copy

def ghost2_fake_move(board, move, current_row,current_col):
    global g2_score
    board_copy=copy.deepcopy(board)
    row, col = move

    if board_copy[row][col]=="P":
        board_copy[current_row][current_col] = " "
        board_copy[row][col] = 'G'
        g2_score+=1000
        evaluate_g1()
        g2_score-=1000
        for row in board_copy:
            print(' '.join(row))
        return board_copy

    elif distance(board, (current_row,current_col))>distance(board, move):
        board_copy[row][col] = 'G'
        g2_score+=1
        evaluate_g2()
        g2_score-=1
        for row in board_copy:
            print(' '.join(row))
        return board_copy 
    
    elif distance(board, (current_row,current_col))==distance(board, move):
        evaluate_g2()
        for row in board_copy:
            print(' '.join(row))
        return board_copy 
    elif distance(board, (current_row,current_col))<distance(board, move):
        board_copy[row][col] = 'G'
        g2_score-=1
        evaluate_g2()
        g2_score+=1
        for row in board_copy:
            print(' '.join(row))
        return board_copy 
    elif (row==current_row) and (col==current_col):
        evaluate_g2()
        for row in board_copy:
            print(' '.join(row))
        return board_copy

def evaluate_g1():
    print(g1_score)
    return g1_score

def evaluate_g2():
    print(g2_score)
    return g2_score

def fake_move(board, move, current_row,current_col):
    global score
    board_copy=copy.deepcopy(board)
    i=0
    for row in board_copy:
        i+=1
    print(i)
    row, col = move
    if board_copy[row][col] == '.':  # Check if the move is valid
        print(type(current_col), type(current_row))
        #print((board_copy[current_row]))
        board_copy[current_row]=' '
        print()
        board_copy[row][col] = 'P'
        score+=9
        evaluate()
        score-=9
        for row in board_copy:
            print(' '.join(row))
        return board_copy 
    
    if board_copy[row][col] == ' ':
        board_copy[current_row][current_col]=' '
        board_copy[row][col] = 'P'  # Assuming 'X' represents the player's move
        score-=1
        evaluate()
        score+=1
        for row in board_copy:
            print(' '.join(row))
        return board_copy  # Move successfully made
    
    if board_copy[row][col] == 'P':
        evaluate()
        for row in board_copy:
            print(' '.join(row))
        return board_copy

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
    if board[row][col] == 'P':
        evaluate()
        for row in board:
            print(' '.join(row))
        return board  # Move successfully made

def evaluate():
    print(score)
    return score

def game_over():
    if find_pacman(board)==0:
        print("Game over!")
        return 1
    else:
        return 0


def get_best_move(board, depth,current_row,current_col):
    best_eval = -1000
    best_move = None
    board_copy=np.full((11,20)," ")
    #board_copy=copy.deepcopy(board)
    for i in range(len(board)):
        for j in range(len(board[0])):
            board_copy[i][j] = board[i][j]
    for move in pacman_possible_moves(board_copy, current_row,current_col):
        new_board = fake_move(board_copy, move, current_row,current_col)
        print(type(pacman_possible_moves(board_copy, current_row,current_col)),type(move),type(move))
        eval = minimax(new_board, depth - 1, "min1")
        #eval = minimax(new_board, depth - 1, "min1")
        if eval > best_eval:
            best_eval = eval
            best_move = move
    make_move(board, best_move, current_row,current_col)
    print(evaluate())
    return best_move


def minimax(board, depth, maximizing_player):

    for row in board:
            print(' '.join(row))

    if (depth == 0 or game_over()==1)and maximizing_player=="max":
        return evaluate()
    if (depth == 0 or game_over()==1)and maximizing_player=="min1":
        return evaluate_g1()
    if (depth == 0 or game_over()==1)and maximizing_player=="min2":
        return evaluate_g2()
    board_copy=copy.deepcopy(board)
    max_eval = -1000
    min_eval = 1000
    if maximizing_player=="max":
        loc=find_pacman(board)
        for move in pacman_possible_moves(board_copy, loc[0],loc[1]):
            new_board = fake_move(board_copy, move,  loc[0],loc[1])
            eval = minimax(new_board, depth - 1, "min1")
            max_eval = max(max_eval, eval)
        for row in board:
            print(' '.join(row))
        return max_eval
    if maximizing_player=="min1":
        loc=find_ghost(board)
        for move in ghost_possible_move(board_copy,0):
            new_board = fake_move(board_copy, move,  loc[0],loc[1])
            #print(type(),type())
            eval = minimax(new_board, depth - 1, "min2")
            min_eval = min(min_eval, eval)
        for row in board:
            print(' '.join(row))
        return min_eval
    if maximizing_player=="min2":
        loc=find_ghost(board)
        for move in ghost_possible_move(board_copy,1):
            new_board = fake_move(board_copy, move,  loc[0],loc[1])
            eval = minimax(new_board, depth - 1, "max")
            min_eval = min(min_eval, eval)
        for row in board:
            print(' '.join(row))
        return min_eval

"""
for row in board:
    print(' '.join(row))"""
