from random import randint
import time
import sys
from threading import Thread

#A single node in a tree of utility nodes
#   each node contains:
#   The utility of the current node
#   A reference to the parent of the current node
#   A list of children to the current node
#   A variable that holds the move
class Node:
    def __init__(self, utility=0, parent=None, move=None, boardState=None):
        self.utility = utility
        self.parent = parent  
        self.move = move
        self.children = []
        self.boardState = boardState

    def add_child(self, child):
        self.children.append(child)

#Constant variable for storing positive infinity
INF = float('inf')

#Constant variable for the utility of five pieces in a row
FIVEROWPOS = 100000
FIVEROWNEG = -100000

#Constant variable for how many seconds can pass before a forced time out should happen 
TIMEOUTAMOUNT = 9

#Variables used in min_max_alpha_beta(), they need to be outside the function to fix error due to encapsulation
bestPath = None
alpha = -INF
beta = INF

#Main function for finding the best path to follow using Min Max with Alpha Beta Pruning
#   Input a tree of Nodes that you wish to search through
#   Function will output the best child Node from the root to follow
def min_max_alpha_beta(node, depthLimit = -1):
    global alpha
    global beta
    global bestPath

    #Function for searching through list and setting the new alpha and bestPath
    #   This exists as its own function as to allow for threading and therefore timeouts 
    def mmab_helper(child):
        global alpha
        global beta
        global bestPath

        bestValue = min_value(child,alpha,beta,0,depthLimit)
        if bestValue > alpha:
            alpha = bestValue
            bestPath = child

    bestPath = None
    alpha = -INF
    beta = INF

    #Threading the search to allow for timeouts after a certain number of seconds
    threads = []
    try:
        for child in node.children:
            t = Thread(target=mmab_helper(child))
            t.start()
            threads.append(t)
            time.sleep(TIMEOUTAMOUNT)
    finally:
        [t.join() for t in threads]

    return bestPath

#Finds the child node with the highest utility while also alpha beta pruning
#   When the bottom of a tree is found, the utility of the Node is returned
#   Then the function works its way back up finding the best one using Min Max 
def max_value(node, alpha, beta, depth, limit):
    if len(node.children) == 0 or (limit>0 and depth>=limit):
        return node.utility
    maxValue = -INF
    children = node.children
    for child in children:
        maxValue = max(maxValue, min_value(child,alpha,beta,depth+1,limit))
        if maxValue >= beta:
            return maxValue
        alpha = max(alpha,maxValue)
    return maxValue

#Finds the child node with the lowest utility while also alpha beta pruning
#   When the bottom of a tree is found, the utility of the Node is returned
#   Then the function works its way back up finding the best one using Min Max 
def min_value(node, alpha, beta, depth, limit):
    if len(node.children) == 0 or (limit>0 and depth>=limit):
        return node
    minValue = INF
    children = node.children
    for child in children:
        minValue = min(minValue, max_value(child,alpha,beta,depth+1,limit))
        if minValue <= alpha:
            return minValue
        beta = min(beta,minValue)
    return minValue

#Helper function to min_max_test(). Prints out the utility of all Nodes in a given list of Nodes
def print_children_test(children):
    children_string = ""
    for child in children:
        children_string = children_string + str(child.utility) + ","
    return children_string

#Test function for min max function. Generates a tree with random utilities 0-12 and then runs min_max_alpha_beta over it
def min_max_test():
    parent = Node()
    for x in range(3):
        node = Node(-INF,parent)
        for y in range(3):
            randomNum = randint(FIVEROWNEG,FIVEROWPOS)
            print(randomNum)
            node.add_child(Node(randomNum,node))
        parent.add_child(node)
    answer = min_max_alpha_beta(parent)
    print(print_children_test(answer.children))

#min_max_test()