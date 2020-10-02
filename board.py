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
    if is_space_on_board(x,y) and is_move_valid(x, y):
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

#Main method 
def main():
    create_board()
    wait_for_go_file()
    
main()

