import numpy as np
class Board:
    def __init__(self, inp):
        self.game_board = np.empty((9,9),dtype = object)
        for x in range(9):
            for y in range(9):
                self.game_board[x][y] = Slot(inp[9*x + y], x, y)
        self.row = [set(
        )for i in range(9)]
        self.grid = [set() for i in range(9)]
        self.column = [set()for i in range(9)]
                
    def __str__(self):
        boardString = ''
        for i in range(9):
            if i%3 == 0: boardString += '                     \n'; #to have a horizontal spacer between grids of nine

            for j in range(9):
                if j%3 == 0: boardString += '   ';#to have vertical spacer between grids of nine

                boardString += f" {self.game_board[i][j]} "#fill in the box with the index of the grid at (row i,column j)

            boardString += '\n'

        return boardString
    
    
#     def PossibleByLine(value,rowOrCol): #returns true when a value does not already exist in an inputted row or column numpy.array(slot)
#         return filter(lambda rowOrColVal: rowOrColVal != value,rowOrCol)
    
    def getRows(self):
        for x in range(9)
            row_taken_values = (slot.value for slot in game_board[x]).remove(0)
            self.row[x] = 
            self.column
        
#     def getColumns(self):
        
#     def getGrids(self):
    
#     def updaterowsandgridandcolumn(self)
#         if slot.possibleValues =1,
#             self.row[slot.row] = slot.possibleValues[0] 
#             self.column[slot.column] = slot.possibleValues[0]
#             self.grid[slot.grid] . remove possible from our grid available values
#             slot.value = slot.updateSlot(slot.possisbleValues[0])
            
#     def nextMove(self):
#         for slot in self.game_board:
#             if len(slot.possibleValues) = 1:
#                 self.updaterowsandgridandcolumn(slot)
#             elif len(slot.possibleValues) > 1:
#                 slot.updatePossibleValues(row[self.row], column[self.column], grid[self.grid])
            
#         self.nextMove()
       
                
class Slot:
    def __init__(self, value,x,y):
        self.row = x
        self.column = y
        self.grid = 3 * (x//3) + (y//3)
        self.value = int(value)
        self.possibleValues = (1,2,3,4,5,6,7,8,9)
    
    def __str__(self):
        return str(self.value)
    
    def getValue(self):
        return self.value
    
    def getPossibleValues(self):
        return self.possiblevalues
    
    def updateSlot(self,value):
        self.value = value
        self.possibleValues = 0
    
    def updatePossibleValues(self, row_values, column_values, grid_values):
        self.possible_values = intersection(row_values, column_values, grid_values)
    


inp_game = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
gameboard = Board(inp_game)
print(gameboard)