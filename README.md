# Sudoku solver (python)
This is a sudoku solver in python. It takes in a 81 long number which represents a sudoku. It solves it and gives you back the answer.

## Installation
1. clone the git repository
```
git clone https://github.com/PukieDiederik/sudoku.py.git
```
2. run the program
```
python3 sudoku.py -s YOUR_SUDOKU_HERE
```

## how to use
The sudoku has to be flattened as a 81 character long number (where you go from top to bottom left to right) and empty cells have to be 0. for example
```
497 200 000
100 400 005
000 016 098
  
620 300 040
300 900 000
001 072 600
  
002 005 870
000 600 004
530 097 061
```
A sudoku like this would become:
```
497200000100400005000016098620300040300900000001072600002005870000600004530097061
```

You can either submit a single sudoku or a file. To submit a single sudoku use the `-s` option with the flattened sudoku behind it. To submit a file use the `-f` option and add the path to your file behind it. This program suspects that each new line of the file is a seperate sudoku.

You can use `-m` to add a maxium amount of sudokus it will solve. `-p` will change the way it prints, by default it is compact but if you want a simple to understand sudoku use `-p pretty`. `--multithreaded` causes the program to utilize multithreading. `-t` shows how long the program took. `-i` shows the id of the sudoku. This is only usefull if you are doing a lot of sudokus and would like some order in it.