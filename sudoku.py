#%% the sudoku itself
class Sudoku:
    #input can be a 81 character long string
    def __init__(self, input : str):
        def parseString(input: str):
            if (len(input) == 81):
                return [int(x) for x in input]
            else:
                print("length of the string was not 81 characters")
                return None

        self.value = parseString(input)

    #this function will also return false if the number is the same at the position
    def checkIfValidAt(self, pos, value):
        if(pos > 80): print("position out of range")
        elif(value > 9): print("value out of range")
        else:
            #if the number is in the same row
            horizontalOffset = pos % 9
            horizontalBase = pos - horizontalOffset

            for x in range(horizontalBase, horizontalBase + 9):
                if(self.value[x] == value): return False

            #if the number is in the same column
            for y in range(horizontalOffset, 81, 9):
                if(self.value[y] == value): return False

            #if the number is in the same section (3x3)
            # vertical section + horizontal section
            sectionStart = (pos - (pos % 27)) + ((pos % 9) - (pos % 3))
            for y in range(sectionStart, 27, 9):
                for x in range(3):
                    if(self.value[x + y] == value): return False

            #if there is no reason why you cant place that number there, return true
            return True

    def getValueAt(self, posx, posy):
        return self.value[posy * 9 + posx]
    
    def printSudoku(self):
        for y in range(9):
            for x in range(9):
                print(self.value[y*9+x], end="")
            print("")
            

#%% this will solve the sudoku (takes in a sudoku as input)
def solveSudoku(sudoku: Sudoku):
    
    return None