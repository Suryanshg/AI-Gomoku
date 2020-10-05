from random import randint

#A single node in a tree of utility nodes
#   each node contains:
#   The utility of the current node
#   A reference to the parent of the current node
#   A list of children to the current node
class Node:
    def __init__(self, utility=0, parent=None):
        self.utility = utility    
        self.parent = parent  
        self.children = []

    def add_child(self, child):
        self.children.append(child)

#Constant variable for storing positive infinity
INF = float('inf')

#Main function for finding the best path to follow using Min Max with Alpha Beta Pruning
#   Input a tree of Nodes that you wish to search through
#   Function will output the best child Node from the root to follow#Main function for finding the best path to follow using Min Max with Alpha Beta Pruning
def min_max_alpha_beta(node):
    bestPath = None
    alpha = -INF
    beta = INF
    children = node.children
    for child in children:
        bestValue = min_value(child,alpha,beta)
        if bestValue > alpha:
            alpha = bestValue
            bestPath = child
    return bestPath

#Finds the child node with the highest utility while also alpha beta pruning
#   When the bottom of a tree is found, the utility of the Node is returned
#   Then the function works its way back up finding the best one using Min Max 
def max_value(node, alpha, beta):
    if len(node.children) == 0:
        return node.utility
    maxValue = -INF
    children = node.children
    for child in children:
        maxValue = max(maxValue, min_value(child,alpha, beta))
        if maxValue >= beta:
            return maxValue
        alpha = max(alpha,maxValue)
    return maxValue

#Finds the child node with the lowest utility while also alpha beta pruning
#   When the bottom of a tree is found, the utility of the Node is returned
#   Then the function works its way back up finding the best one using Min Max 
def min_value(node, alpha, beta):
    if len(node.children) == 0:
        return node
    minValue = INF
    children = node.children
    for child in children:
        minValue = min(minValue, max_value(child,alpha,beta))
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
            randomNum = randint(0,12)
            print(randomNum)
            node.add_child(Node(randomNum,node))
        parent.add_child(node)
    answer = min_max_alpha_beta(parent)
    print(print_children_test(answer.children))

min_max_test()