from enum import Enum
import os.path
from os import path
import sys
import random
from time import sleep

#Name of our group, using TEST as a place holder
groupName = "TEST"

# Num moves played by TEST
movesPlayed = 0

ourTeam = 1

#Enum for every state a board space can be in
#    Empty = Space is empty
#    Blue = A blue piece (Team 1) is on the space
#    Orange = A orange piece (Team 2) is on the space
class SpaceState(Enum):
    EMPTY = 0
    BLUE = 1
    ORANGE = 2

# Width and Height of the game board
boardSize = 15

#Variable used to store the game board
#The game board is stored as a 2D array of SpaceStates 
board = []

#Number used for converting chars to ints and vice versa
charOffset = 97

#Fills the board with empty spaces 
def create_board():
    global board
    board = [[SpaceState.EMPTY for _ in range(15)] for _ in range(15)]

#Prints out the values of every space of the board in a easier to read format for any testing/debugging needs
def print_board():
    print("Board is:")
    for row in board:
        for elem in row:
            print(elem.value, end=', ')
        print()

#Returns if a piece can be placed on the specified space
def is_move_valid(x:int, y:int):
    return board[y][x] == SpaceState.EMPTY

# returns if the specified space is actually oon the board
def is_space_on_board(x:int, y:int):
   return (x >= 0 and x < boardSize) and (y >= 0 and y < boardSize)

#Place a team's piece at the specified x and y coordinates
#If the space is already taken up by a piece then an error is printed and the piece is not placed 
def place_piece(x:int, y:int, team:int):
    global board
    global movesPlayed
    if not is_move_valid(x,y) and team == 2 and movesPlayed==0:
        board[y][x] = SpaceState(team)   
    elif is_space_on_board(x,y) and is_move_valid(x, y):
        board[y][x] = SpaceState(team)
    else:
        print("INVALID MOVE AT: %i,%i" % (x, y))

#Tests place_piece() to make sure it places pieces in the correct spots and returns errors when needed
def placement_test():
    place_piece(1,1,2)
    place_piece(2,2,1)
    place_piece(3,3,2)
    place_piece(3,3,1)
    place_piece(3,4,1)

#Test function
def test():
    create_board()
    placement_test()
    print_board()
    
#Turns inputted letter into a number corresponding to the boards x coordinate 
#   i.e: A -> 0
def letter_to_int(letter):
    letter.lower()
    return ord(letter) - charOffset

#Loop that waits for our teams .go file to appear in the current directory
def wait_for_go_file():
    exists = path.exists(groupName + ".go")
    while(not exists):
        exists = path.exists(groupName + ".go")
    endGameFileExists = path.exists('end_game') # Checks if the end game file exists
    if(endGameFileExists): # if the end game file exist, then game is over
        print("Game is over! Moves played by TEST are: "+str(movesPlayed))
        sys.exit()
    else:
        parse_move_file()

#Delete the .go file for our team
def delete_go_file():
    exists = path.exists(groupName + ".go")
    while(not exists):
        exists = path.exists(groupName + ".go")
    os.remove(groupName + ".go")

#Parses through the move file and places a piece in the corresponding space on the board
def parse_move_file():
    global ourTeam
    exists = path.exists('move_file')
    while(not exists):
        exists = path.exists('move_file')
    with open('move_file', 'r') as file:
        fileRead = file.read().replace('\n', '')
    if(len(fileRead)>0): # There exists a move already
        move = fileRead.split()
        
        oppTeam = 2
        if move[0] != groupName:
            ourTeam = 2
            oppTeam = 1

        place_piece(letter_to_int(move[1]), int(move[2])-1,oppTeam)
    # else: # No move already exists (our program is Player 1)  
    generate_and_place_random(ourTeam)

#Generates a random move and places
def generate_and_place_random(ourTeam):
    x = random.randint(0,14)
    y = random.randint(0,14)
    while not is_move_valid(x, y):
        x = random.randint(0,14)
        y = random.randint(0,14)
    place_piece(x,y,ourTeam)
    global movesPlayed
    movesPlayed+=1
    x = int_to_letter(x)
    y = y + 1

    with open('move_file','w') as mf: # Writing the move back to file
        mf.write(groupName+" "+x+" "+str(y))
    
    print_board()
    delete_go_file()
    sleep(0.5) # Sleep for 500 ms (Waiting for deletion of our team's .go file)
    # if(movesPlayed==1):
    #     sys.exit()
    wait_for_go_file()

# Maps an integer to respective columns name, ex. 0 -- > A
def int_to_letter(col):
    return chr(col + charOffset)


# Returns the eval value for rows
def row_eval(board, team):
    board_size = 15

    # Dictionary that takes into account [NumOfPieces : [WithZeroOpenedPlaces, WithOneOpenedPlaces, WithTwoOpenedPlaces]]
    board_count = {1:[0,0,0], 2:[0,0,0], 3:[0,0,0], 4:[0,0,0]}

    for y in range(board_size):
        # x = 0      
        # start_ind = 0
        # end_ind = 0        
        for x in range(board_size):
            consec = 0 # Track of Consecutives in a row
            open_ends = 0 # Track of respective opened space with consecutives
            if board[y][x] == team:
                if x > 0: # Check for the boundary conditions
                    if board[y][x-1] == 0: # If empty, means an opened space
                        open_ends += 1
                consec += 1

                i = 1           

                # Lets check for the consecutives after the current piece
                while True:
                    if x+i < board_size:
                        if board[y][x+i] == team: # Increase the consecutives
                            consec += 1
                        elif board[y][x+i] != team: # Check for opened spaces and stop
                            if board[y][x+i] == 0:
                                open_ends += 1
                            break
                    elif x+i == board_size: # Stops at the boundary condition
                        break  
                    i += 1

                if 0 < consec < 5 and open_ends > 0: # If not the winning condition in a row
                    board_count[consec][open_ends] += 1 # Update the dictionary
                elif consec == 5: # If winning condition in a row
                    return 1000000
                # print(x)
                # print(board_count)

                # Resetting the consecutive count and the opened spaces count before going backwards
                consec = 1
                open_ends = 0

                if x < board_size: # Check for the boundary conditions
                    if board[y][x+1] == 0: # If empty, means an opened space
                        open_ends += 1

                j = 1

                # Lets check for the consecutives before the current piece
                while True:
                    if x-j >= 0:
                        if board[y][x-j] == team:  # Increase the consecutives
                            consec += 1
                        elif board[y][x-j] != team: # Check for opened spaces and stop
                            if board[y][x-j] == 0:
                                open_ends += 1
                            break
                    elif x-j < 0: # Stops at the boundary condition
                        break  
                    j += 1
                
                if 0 < consec < 5 and open_ends > 0:  # If not the winning condition in a row
                    board_count[consec][open_ends] += 1 # Update the dictionary
            #     print(board_count)

            # print("-------------------------------------------")
    # Lets evaluate on the basis of data about consecutive pieces and opened spaces
    print(board_count)
    row_eval = 0.0
    for consecs in board_count:
        for i in range(len(board_count[consecs])):
            w = assign_weights(consecs, i) # Acquire the respective weights
            row_eval += board_count[consecs][i] * w # Calculate the weighted sum

    return row_eval

# Returns the eval value for columns
def col_eval(board, team):
    board_size = 15

    # Dictionary that takes into account [NumOfPieces : [WithZeroOpenedPlaces, WithOneOpenedPlaces, WithTwoOpenedPlaces]]
    board_count = {1:[0,0,0], 2:[0,0,0], 3:[0,0,0], 4:[0,0,0]}

    for y in range(board_size):
        # x = 0      
        # start_ind = 0
        # end_ind = 0        
        for x in range(board_size):
            consec = 0 # Track of Consecutives in a row
            open_ends = 0 # Track of respective opened space with consecutives
            if board[x][y] == team:
                if x > 0: # Check for the boundary conditions
                    if board[x-1][y] == 0: # If empty, means an opened space
                        open_ends += 1
                consec += 1

                i = 1

                # Lets check for the consecutives after the current piece
                while True:
                    if x+i < board_size:
                        if board[x+i][y] == team: # Increase the consecutives
                            consec += 1
                        elif board[x+i][y] != team: # Check for opened spaces and stop
                            if board[x+i][y] == 0:
                                open_ends += 1
                            break
                    elif x+i == board_size: # Stops at the boundary condition
                        break  
                    i += 1

                if 0 < consec < 5 and open_ends > 0: # If not the winning condition in a row
                    board_count[consec][open_ends] += 1 # Update the dictionary
                elif consec == 5: # If winning condition in a row
                    return 1000000
                # print(x)
                # print(board_count)

                # Resetting the consecutive count and the opened spaces count before going backwards
                consec = 1
                open_ends = 0

                if x < board_size: # Check for the boundary conditions
                    if board[x+1][y] == 0: # If empty, means an opened space
                        open_ends += 1

                j = 1

                # Lets check for the consecutives before the current piece
                while True:
                    if x-j >= 0:
                        if board[x-j][y] == team:  # Increase the consecutives
                            consec += 1
                        elif board[x-j][y] != team: # Check for opened spaces and stop
                            if board[x-j][y] == 0:
                                open_ends += 1
                            break
                    elif x-j < 0: # Stops at the boundary condition
                        break  
                    j += 1

                
                if 0 < consec < 5 and open_ends > 0:  # If not the winning condition in a row
                    board_count[consec][open_ends] += 1 # Update the dictionary
            #     print(board_count)

            # print("-------------------------------------------")
    
    # Lets evaluate on the basis of data about consecutive pieces and opened spaces
   
    print(board_count)
    col_eval = 0.0
    for consecs in board_count:
        for i in range(len(board_count[consecs])):
            w = assign_weights(consecs, i) # Acquire the respective weights
            col_eval += board_count[consecs][i] * w # Calculate the weighted sum

    return col_eval

# Board for testing the Eval function
test_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]

def diag_eval(board, team):
    board_size = 15

    # Dictionary that takes into account [NumOfPieces : [WithZeroOpenedPlaces, WithOneOpenedPlaces, WithTwoOpenedPlaces]]
    board_count = {1:[0,0,0], 2:[0,0,0], 3:[0,0,0], 4:[0,0,0]}

    for y in range(board_size):  
        for x in range(board_size):
            consec = 0 # Track of Consecutives in a row
            open_ends = 0 # Track of respective opened space with consecutives
            if board[y][x] == team:
                if x > 0 and y > 0: # Check for the boundary conditions
                    if board[y-1][x-1] == 0: # If empty, means an opened space
                        open_ends += 1
                consec += 1

                i = 1           

                # Lets check for the consecutives after the current piece
                while True:
                    if x+i < board_size and y + i < board_size:
                        if board[y+i][x+i] == team: # Increase the consecutives
                            consec += 1
                        elif board[y+i][x+i] != team: # Check for opened spaces and stop
                            if board[y+i][x+i] == 0:
                                open_ends += 1
                            break
                    elif x+i == board_size or y+i == board_size: # Stops at the boundary condition
                        break  
                    i += 1

                if 0 < consec < 5 and open_ends > 0: # If not the winning condition in a row
                    board_count[consec][open_ends] += 1 # Update the dictionary
                elif consec == 5: # If winning condition in a row
                    return 1000000
                print(x)
                print(board_count)

                # Resetting the consecutive count and the opened spaces count before going backwards
                consec = 1
                open_ends = 0

                if x < board_size - 1 and y < board_size -1: # Check for the boundary conditions
                    if board[y+1][x+1] == 0: # If empty, means an opened space
                        open_ends += 1

                j = 1

                # Lets check for the consecutives before the current piece
                while True:
                    if x-j >= 0 and y- j >= 0:
                        if board[y-j][x-j] == team:  # Increase the consecutives
                            consec += 1
                        elif board[y-j][x-j] != team: # Check for opened spaces and stop
                            if board[y-j][x-j] == 0:
                                open_ends += 1
                            break
                    elif x-j < 0 and y-j < 0: # Stops at the boundary condition
                        break  
                    j += 1
                
                if 0 < consec < 5 and open_ends > 0:  # If not the winning condition in a row
                    board_count[consec][open_ends] += 1 # Update the dictionary
                elif consec == 5: # If winning condition in a row
                    return 1000000
                print(board_count)

    #_--------------------------------------------------------------------------------------------------------------------------
                consec = 1
                open_ends = 0

                if x > 0 and y < board_size - 1: # Check for the boundary conditions
                    if board[y+1][x-1] == 0: # If empty, means an opened space
                        open_ends += 1
               

                k = 1           

                # Lets check for the consecutives after the current piece
                while True:
                    if x+k < board_size - 1 and y - k > 0:
                        if board[y-k][x+k] == team: # Increase the consecutives
                            consec += 1
                        elif board[y-k][x+k] != team: # Check for opened spaces and stop
                            if board[y-k][x+k] == 0:
                                open_ends += 1
                            break
                    elif x+k == board_size or y-k == 0: # Stops at the boundary condition
                        break  
                    k += 1

                if 0 < consec < 5 and open_ends > 0: # If not the winning condition in a row
                    board_count[consec][open_ends] += 1 # Update the dictionary
                elif consec == 5: # If winning condition in a row
                    return 1000000
                
                print(board_count)

                # Resetting the consecutive count and the opened spaces count before going backwards
                consec = 1
                open_ends = 0

                if x < board_size - 1 and y > 0: # Check for the boundary conditions
                    if board[y-1][x+1] == 0: # If empty, means an opened space
                        open_ends += 1

                j = 1

                # Lets check for the consecutives before the current piece
                while True:
                    if x-j > 0 and y + j < board_size - 1:
                        if board[y+j][x-j] == team:  # Increase the consecutives
                            consec += 1
                        elif board[y+j][x-j] != team: # Check for opened spaces and stop
                            if board[y+j][x-j] == 0:
                                open_ends += 1
                            break
                    elif x-j < 0 or y+j > board_size: # Stops at the boundary condition
                        break  
                    j += 1
                
                if 0 < consec < 5 and open_ends > 0:  # If not the winning condition in a row
                    board_count[consec][open_ends] += 1 # Update the dictionary
                elif consec == 5: # If winning condition in a row
                    return 1000000
                print(board_count)

            print("-------------------------------------------")
    # Lets evaluate on the basis of data about consecutive pieces and opened spaces
    print(board_count)
    diag_eval = 0.0
    for consecs in board_count:
        for i in range(len(board_count[consecs])):
            w = assign_weights(consecs, i) # Acquire the respective weights
            diag_eval += board_count[consecs][i] * w # Calculate the weighted sum

    return diag_eval

# Assigns weights to different cases of consecutive pieces and opened nodes in them, 
# l -- The number of consecutive pieces
# o -- The number of associated opened spaces
def assign_weights(l, o):
    w_o = 0 
    if l == 4:
        if o == 2:
            w_o = 26.6
        elif o == 1:
            w_o = 13.3
        elif o == 0:
            w_o = 0
    elif l == 3:
        if o == 2:
            w_o = 20
        elif o == 1:
            w_o = 10
        elif o == 0:
            w_o = 0
    elif l == 2:
        if o == 2:
            w_o = 13.3
        elif o == 1:
            w_o = 6.6
        elif o == 0:
            w_o = 0
    elif l == 1:
        if o == 2:
            w_o = 6.6
        elif o == 1:
            w_o = 3.3
        elif o == 0:
            w_o = 0
    return w_o


#Main method 
def main():
    create_board()
    wait_for_go_file()
    
#main()

test = diag_eval(test_board,1)
print(test)