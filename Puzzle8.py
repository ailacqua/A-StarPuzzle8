"""
Solves 8 puzzle using A-Star

Checks to ensure inputted board status is solvable, then solves using A-Star algorithm

Author: Alex Ilacqua
Date: 1/22/2023
"""
from copy import deepcopy

#defining node class
class Node:
    #creating node constructor
    def __init__(self,board,level,children,parent,move):
        self.board = board
        self.level = level
        #calculating manhattan distance and f(n)
        self.calcH()
        self.calcF()
        self.children = children
        self.parent = parent
        self.move = move
    #finds direction of any move from old to new coordinates
    def findMoveDir(self,oldR,newR,oldC,newC):
        if newR == oldR and newC == oldC + 1:
            move = "right"
        if newR == oldR and newC == oldC - 1:
            move = "left"
        if newR == oldR + 1 and newC == oldC:
            move = "down"
        if newR == oldR - 1 and newC == oldC:
            move = "up"
        return move
    #expands node with children    
    def expand(self):
        children = []
        delList = []
        #finds row and column of blank space location
        for i in range(0,len(self.board)):
            for j in range(0,len(self.board)):
                if self.board[i][j] == 0:
                    r=i
                    c=j
        #establishes list of possible coordinates where blank can move to
        options = [[r,c-1,"left"],[r,c+1,"right"],[r-1,c,"up"],[r+1,c,"down"]]
        #deletes the possible coordinate if r and c are greater than 2 or less than 0
        for i in range(0,len(options)):
            for j in range(0,len(options[i])-1):
                if (options[i][j] > len(self.board)-1) or (options[i][j] < 0):
                    delList.append(i)
        #reverses delete list to remove index out of bounds error
        delList.reverse()
        #deletes impossible move options
        for i in delList:
            del options[i]
        for i in range(0,len(options)):
            #creates new board with new blank space move
            newBoard = deepcopy(self.board)
            temp = newBoard[options[i][0]][options[i][1]]
            newBoard[options[i][0]][options[i][1]] = 0
            newBoard[r][c] = temp
            #finds move direction
            moveDir = options[i][2]
            #creates list of children nodes with new board states
            children.append(Node(newBoard,self.level+1,None,self,moveDir))
        #returns list of children
        return children
    #calculates F    
    def calcF(self):
        #adds level (g) and manhattan distance (h) to find f
        self.f = self.h + self.level
    #calculates manhattan distance    
    def calcH(self):
        mhd = 0
        #finds sum of x and y displacement from ideal position for all board items
        for i in range(0,len(self.board)):
            for j in range(0,len(self.board)):
                mhd = mhd + (abs(self.board[i][j]%3 - j)+abs(self.board[i][j]//3 - i))
        #sets h to mhd
        self.h = mhd

#finds if board is solvable
def isSolvable(puzzle):
    numbers = []
    inv = 0
    #finds row number of blank space
    for i in range(0,len(puzzle)):
        for j in range(0,len(puzzle)):
            numbers.append(puzzle[i][j])
            if puzzle[i][j] == 0:
                rowBlank = i
    #if the board total is odd
    if (len(numbers) % 2) != 0:
        numbers.remove(0)
        #finds total number of inversions present in the board
        for i in range(0,len(numbers)):
            current = numbers[i]
            for j in range(0,i+1):
                if numbers[j] > current:
                    inv = inv + 1
        #if the inversions are even then the board is solvable
        if inv % 2 == 0:
            return True
        else:
            return False
    else:
        numbers.remove(0)
        #finds total number of inversions present in the board
        for i in range(0,len(numbers)):
            current = numbers[i]
            for j in range(0,i+1):
                if numbers[j] > current:
                    inv = inv + 1
        #adds blank space row
        inv = inv + rowBlank
        #if inversions plus blank space row are odd then it is solvable
        if inv % 2 != 0:
            return True
        else:
            return False
#prints path and moves to solution        
def printPath(node):
    current = node
    moves = []
    #loops and adds moves to list until initial state is hit
    while current.parent != None:
        moves.append(current.move)
        current = current.parent
    moves.reverse()
    #prints the moves
    print("The moves are:")
    for move in moves:
        print(move, end=", ")    
#primar aStar algorithm
def aStar(puzzle):
    #initializes the start node
    start = Node(puzzle,0,None,None,None)
    #finds if puzzle is solvable
    if isSolvable(puzzle) == False:
        print("This puzzle is unsolvable! Please try again.")
    else:
        #creating unvisited and visited lists
        unvisited = [start]
        visited = []
        #algorithm continues until unvisited list is empty
        while len(unvisited) != 0:
            print(len(unvisited))
            #sorts the unvisited list by the value of f
            unvisited.sort(key=lambda node:node.f)
            #stops algorithm and prints solution if goal state met
            if unvisited[0].h == 0:
                print("Solution found!")
                print("Number of moves:" + str(unvisited[0].level))
                printPath(unvisited[0])
                break
            #finds children for node with least f
            children = unvisited[0].expand()
            #loops through children
            for child in children:
                best = True
                #if there is same node in unvisited list, current node is not the best
                for item in unvisited:
                    if item.board == child.board and item.f == child.f:
                        best = False
                #if there is same node in visited list, current node is not the best
                for item in visited:
                    if item.board == child.board and item.f == child.f:
                        best = False
                #appends node only if it is the best node
                if best == True:
                    unvisited.append(child)
            #deletes the best f node
            del unvisited[0]
            #appends best f node to unvisited
            visited.append(unvisited[0])

#takes input puzzle
def takeInput():
    #adds new input to starting pos array based on location
    startingPos = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(0,3):
        for j in range(0,3):
            startingPos[i][j] = int(input("Enter tile " + str(i) + " " + str(j) + ": "))
    print("The starting position is:")
    print(startingPos)
    print("Developing solution...")
    #returns startingpos
    return startingPos
    
def main():
    #establishes goal state, takes input and runs a*
    goalState = [[0,1,2],[3,4,5],[6,7,8]]
    puzzle = [[8,3,2],[4,7,1],[0,5,6]]
    puzzle = takeInput()
    aStar(puzzle)
    
main()