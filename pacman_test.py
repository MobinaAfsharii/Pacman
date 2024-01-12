from pacman import *

print("-------------------------------test board---------------------------")
for row in board:
    print(' '.join(row))
print(type(board))

print("-------------------------------set ghosts and pacman---------------------------")
ghost1=Ghost(1,11)
ghost2=Ghost(5,9)
board[9][1]='P'
for row in board:
    print(' '.join(row))
print(type(board))

print("-------------------------------ghost move---------------------------")
ghost1.move()
ghost2.move()
for row in board:
    print(' '.join(row))
print(type(board))

print("-------------------------------ghosts location---------------------------")
ghosts_location = find_ghost(board)
print("first :",ghosts_location[0])
print("second :",ghosts_location[1])
print(type(ghosts_location))

print("-------------------------------pacman location---------------------------")
pacman_location = find_pacman(board)
print("pacman :",pacman_location)
print(type(pacman_location))

print("-------------------------------pacman distance---------------------------")
print(distance(board,ghosts_location[0]))
print(type(distance(board,ghosts_location[0])))

print("-------------------------------ghost possible moves---------------------------")
print("first ghost possible moves:")
print(ghost_possible_move(board,0))
print(type(ghost_possible_move(board,0)))
print("\nsecond ghost possible moves:")
print(ghost_possible_move(board,1))
print(type(ghost_possible_move(board,1)[0]))

print("-------------------------------pacman possible moves---------------------------")
print("pacman possible moves:")
print(pacman_possible_moves(board,pacman_location[0],pacman_location[1]))
print(type(pacman_possible_moves(board,pacman_location[0],pacman_location[1])))

print("-------------------------------first ghost fake move---------------------------")
ghost1_fake_move(board,[9,1],ghosts_location[0][0],ghosts_location[0][1])
print(type(ghost1_fake_move(board,[9,1],ghosts_location[0][0],ghosts_location[0][1])))

print("-------------------------------second ghost fake move---------------------------")
ghost1_fake_move(board,(9,1),ghosts_location[1][0],ghosts_location[1][1])
print(type(ghost1_fake_move(board,[9,1],ghosts_location[1][0],ghosts_location[1][1])))

print("-------------------------------evaluate first ghost score---------------------------")
evaluate_g1()
print(type(evaluate_g1()))

print("-------------------------------evaluate second ghost score---------------------------")
evaluate_g2()
print(type(evaluate_g2()))

print("-------------------------------pacman fake move---------------------------")
fake_move(board,[1,1],pacman_location[0],pacman_location[1])
print(type(fake_move(board,[1,1],pacman_location[0],pacman_location[1])))

print("-------------------------------pacman move---------------------------")
#make_move(board,(1,1),pacman_location[0],pacman_location[1])
#print(type(make_move(board,(1,1),pacman_location[0],pacman_location[1])))

print("-------------------------------evaluate pacman score---------------------------")
evaluate()
print(type(evaluate()))

print("-------------------------------Game over---------------------------")
if game_over()==0:
    print("continue")
print(type(game_over()))


print("-------------------------------get best move---------------------------")
ghost1.move()
ghost2.move()
get_best_move(board,4,pacman_location[0],pacman_location[1])
