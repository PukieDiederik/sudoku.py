#%% imports
from copy import deepcopy
import sys
import os
import re
import time #for testing speed of the program
import multiprocessing as mp

#%% the sudoku itself
class Sudoku:
    #input can be a 81 character long string
    def __init__(self, input):
        if(type(input) == str):
            if (len(input) == 81):
                self.value = [int(x) for x in input]
            else:
                print("length of the input was not 81 characters")
                self.value = None

        elif(type(input) == list):
            if(len(input) == 81):
                self.value = input
            else:
                print("length of the input was not 81 characters")
                self.value = None

    def __deepcopy__(self, memo):
        return type(self)(deepcopy(self.value))

    def checkIfValidAt(self, pos : int, value: int) -> bool:
        if(pos > 80): print("position out of range")
        else:
            #check if number is more than 9
            if (value > 9): return False

            #if the number is in the same row
            horizontalOffset = pos % 9
            horizontalBase = pos - horizontalOffset

            for x in range(horizontalBase, horizontalBase + 9):
                if(self.value[x] == value and x != pos): return False

            #if the number is in the same column
            for y in range(horizontalOffset, 81, 9):
                if(self.value[y] == value and y != pos): return False

            #if the number is in the same section (3x3)
            # vertical section + horizontal section
            sectionStart = (pos - (pos % 27)) + ((pos % 9) - (pos % 3))
            for y in range(sectionStart, sectionStart + 27, 9):
                for x in range(3):
                    if(self.value[x + y] == value and x + y != pos): return False

            #if there is no reason why you cant place that number there, return true
            return True

    def getValueAt(self, posx, posy):
        return self.value[posy * 9 + posx]
    
    def printSudoku(self):
        for y in range(9):
            for x in range(9):
                print(self.value[y*9+x], end="")
            print("")

    def getSudokuString(self):
        s = ""
        for i in range(81):
            s += str(self.value[i])
        return s
            

#%% this will solve the sudoku (takes in a sudoku as input)
def solveSudoku(sudoku: Sudoku):
    unsolvedSudoku = deepcopy(sudoku)
    currentPos = 0
    direction = 1 #1 forward, -1 backward
    #loop until finished
    while(0 <= currentPos < 81):
        if(sudoku.value[currentPos] != 0): currentPos += direction
        else:
            direction = 1
            #search for the next valid position
            unsolvedSudoku.value[currentPos] += 1
            while not (unsolvedSudoku.checkIfValidAt(currentPos, unsolvedSudoku.value[currentPos])):
                unsolvedSudoku.value[currentPos] += 1
                if (unsolvedSudoku.value[currentPos] > 9):
                    unsolvedSudoku.value[currentPos] = 0
                    direction = -1
                    currentPos -= 1
                    break

            if (direction == 1):
                currentPos += 1

    return unsolvedSudoku

# %%
def getSudokusFromFile(path : str, maxLines : int = 0) -> list:
    file = open(path)
    sudokus = []
    if(maxLines == 0):
        values = file.readlines()
        sudokus = [Sudoku(x) for x in (s.rstrip("\n\r") for s in values) if(re.match("^\d{81}$", x))]
    else:
        sudokus = [Sudoku(x) for x in (s.rstrip("\n\r") for s in (file.readline() for i in range(maxLines))) if(x and re.match("^\d{81}$", x))]
    return sudokus

# %%
if (__name__ == "__main__"):
    if(len(sys.argv) > 1):
        maxSudokus = 10000     #this is for large files to prevent it taking 3 days to solve all sudokus
        printType = "regular" # options: pretty (using printSudoku()), regular (sudokus on 2 lines (input and solved)), compact (all on 1 line)
        multiThreaded = False # if the program will be multithreaded

        #TODO: parse options

        #the first argument will always be the sudoku (or a path to it)
        if(re.match("^\d{81}$", sys.argv[1])):
            sudoku = Sudoku(sys.argv[1])
            solved = solveSudoku(sudoku)
            print("input sudoku:  " + sys.argv[1])
            print("solved sudoku: " + solved.getSudokuString())
        elif(os.path.isfile(sys.argv[1])):
            def __mapfunction__(sud):
                return (sud, solveSudoku(sud))

            startTime = time.time()
            sudokus = getSudokusFromFile(sys.argv[1], maxSudokus)
            pool = mp.Pool(12)
            solved = pool.map(__mapfunction__, sudokus)
            endTime = time.time()
            # for x in solved:
            #     print(x[0].getSudokuString() + "," + x[1].getSudokuString())
            print("finished in: " + str(endTime - startTime) + " sec")


        else:
            print("Sudoku is either: not a valid sudoku OR not a valid path")
        
    else:
        print("Not enough arguments")