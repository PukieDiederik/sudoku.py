#%% imports
from copy import deepcopy
import os
import re
import time #for testing speed of the program
import math
import multiprocessing as mp
import argparse

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

    #printing Sudoku functions
    def prettyPrint(unsolved, solved, showId ,id = 0, maxSudokus = 0):
        if(showId): print(f"current sudoku: [{id}/{maxSudokus}]")
        print("  unsolved:        solved:")
        for y1 in range(3):
            print("╬═══╬═══╬═══╬   ╬═══╬═══╬═══╬")
            for y2 in range(3):
                pos = ((y1 * 3) + y2) * 9
                #print unsolved
                print("║", end="")
                for x in range(9):
                    print(str(unsolved.value[pos + x]), end="")
                    if ((x+1) % 3 == 0): print("║", end="")
                print("   ", end="")
                
                #print solved
                print("║", end="")
                for x in range(9):
                    print(str(solved.value[pos + x]), end="")
                    if ((x+1) % 3 == 0): print("║", end="")
                print("")
        print("╬═══╬═══╬═══╬   ╬═══╬═══╬═══╬")

    def compactPrint(unsolved, solved, showId ,id = 0, maxSudokus = 0):
        print("{}{},{}".format(f"[{id}/{maxSudokus}]" if showId else "", "".join(str(i) for i in unsolved.value), "".join(str(i) for i in solved.value)))

#%% this will solve the sudoku (takes in a sudoku as input)
def solveSudoku(sudoku: Sudoku):
    unsolvedSudoku = deepcopy(sudoku)
    currentPos = 0
    direction = 1 #1 forward, -1 backward
    #loop until finished
    while(0 <= currentPos < 81):
        if(sudoku.value[currentPos] != 0): currentPos += direction # skip if there is a constant number
        else:
            direction = 1
            #search for the next valid position
            unsolvedSudoku.value[currentPos] += 1
            while not (unsolvedSudoku.checkIfValidAt(currentPos, unsolvedSudoku.value[currentPos])) and unsolvedSudoku.value[currentPos] <=9:
                unsolvedSudoku.value[currentPos] += 1

            if (unsolvedSudoku.value[currentPos] <= 9):
                currentPos += 1
            else:
                unsolvedSudoku.value[currentPos] = 0
                direction = -1
                currentPos -= 1

    return unsolvedSudoku

# %%
def getSudokusFromFile(path : str, maxLines : int = 0) -> list:
    file = open(path)
    sudokus = []
    if(maxLines <= 0):
        values = file.readlines()
        sudokus = [Sudoku(x) for x in (s.rstrip("\n\r") for s in values) if(re.match("^\d{81}$", x))]
    else:
        sudokus = [Sudoku(x) for x in (s.rstrip("\n\r") for s in (file.readline() for i in range(maxLines))) if(x and re.match("^\d{81}$", x))]
    return sudokus

# %%
if (__name__ == "__main__"):
    #parsing arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-s", help="input as an 81 digit long string where 0 represents an empty spot, seperate each sudoku with a space", type=str, dest="sudokus", nargs="*")
    argParser.add_argument("-f", help="input as a file with sudokus, seperate multiple files with spaces", type=str, dest="files", nargs="*")

    argParser.add_argument("-m", "--maxSudokus", help="max amount of sudokus, DEFAULT: 100", type=int, default=100)
    argParser.add_argument("-p", "--printType" , help="the way it prints the answer, possible options: compact, pretty, none", type=str, default="compact")
    argParser.add_argument("--multiThreaded", help="uses multithreading, thread count can be given as an additional argument", nargs="?", default=False, const=math.floor(os.cpu_count()/2), type=int)
    argParser.add_argument("-t", "--timed", help="prints statistics on how fast the program is", action="store_true", default=False)
    argParser.add_argument("-i", "--showId", help="shows the id of the sudoku when printing", dest="showId", action="store_true", default=False)
    args = argParser.parse_args()

    #load in the sudokus
    sudokus = []
    if (args.sudokus):
        sudokus = [Sudoku(sudoku) for sudoku in args.sudokus if(re.match("^\d{81}$", sudoku))]
    if(len(sudokus) > args.maxSudokus):
        sudokus = sudokus[:args.maxSudokus]
    
    if(args.files):
        for path in args.files:
            if(os.path.isfile(path)):
                sudokus.extend(getSudokusFromFile(path, args.maxSudokus - len(sudokus)))
            else: print(f"\'{path}\' isnt a valid file path")

    printFunction = None
    if(args.printType == "compact"):
        printFunction = Sudoku.compactPrint
    elif(args.printType == "pretty"):
        printFunction = Sudoku.prettyPrint
    elif(args.printType == "none"):
        printFunction = None
    else:
        print(f"\'{args.printType}\' is not a valid printType")


    solved = []
    startTime = time.time()
    if(args.multiThreaded):
        def __mapfunction__(sud):
            return (sud, solveSudoku(sud))
            
        pool = mp.Pool(args.multiThreaded)
        solved = pool.map(__mapfunction__, sudokus)
    else:
        solved = [(s, solveSudoku(s)) for s in sudokus]
    endTime = time.time()

    if(args.showId):
        for x in range(len(solved)):
            printFunction(solved[x][0],solved[x][1], True, x + 1, len(solved))
    else:
        if(printFunction != None):
            for x in solved:
                printFunction(x[0],x[1], False)
    if(args.timed): print("finished in: " + str(endTime - startTime) + " sec")
# %%
