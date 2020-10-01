from enum import Enum
import os.path
from os import path
import sys
import random

#Name of our group, using TEST as a place holder
groupName = "TEST"

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

#Fills the board with empty spaces 
def create_board():
    global board
    board = [[SpaceState.EMPTY for _ in range(15)] for _ in range(15)]

#Prints out the values of every space of the board in a easier to read format for any testing/debugging needs
def print_board():
    for row in board:
        for elem in row:
            print(elem.value, end=', ')
        print()

#Returns if a piece can be placed on the specified space
def is_move_valid(x:int, y:int):
    return board[y][x] == SpaceState.EMPTY

#Place a team's piece at the specified x and y coordinates
#If the space is already taken up by a piece then an error is printed and the piece is not placed 
def place_piece(x:int, y:int, team:int):
    global board
    if is_move_valid(x, y-1):
        board[y-1][x] = SpaceState(team)
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
    return ord(letter) - 65

#Loop that waits for our teams .go file to appear in the current directory
def wait_for_go_file():
    exists = path.exists(groupName + ".go")
    while(not exists):
        exists = path.exists(groupName + ".go")
    endGameFileExists = path.exists('end_game') # Checks if the end game file exists
    if(endGameFileExists): # if the end game file exist, then game is over
        print("Game is over!")
        sys.exit()
    else:
        parse_move_file()

#Parses through the move file and places a piece in the corresponding space on the board
def parse_move_file():
    exists = path.exists('move_file')
    while(not exists):
        exists = path.exists('move_file')
    with open('move_file', 'r') as file:
        fileRead = file.read().replace('\n', '')
    if(len(fileRead)>0): # There exists a move already
        move = fileRead.split()
        team = 1
        if move[0] != groupName:
            team = 2
        place_piece(letter_to_int(move[1]), int(move[2]),team)
    else: # No move already exists (our program is Player 1)
        team = 1  
    move_to_write = generate_and_place_random(team)

#Generates a random move and places
def generate_and_place_random(team):
    x = random.randint(0,14)
    y = random.randint(0,14)
    place_piece(x,y,team)
    return (x,y)

#Main method 
def main():
    create_board()
    wait_for_go_file()
    print_board()
main()

