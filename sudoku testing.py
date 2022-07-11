import numpy as np
class Board:
    def __init__(self, inp):
        self.gameboard = np.empty((9,9),dtype = object)
        for x in range(9):
            for y in range(9):

                self.game_board[x][y] = Slot(inp[9*x + y], x, y)
                if inp[9*x+y] != 0:
                    self.game_board[x][y].possible_values = {0}
        self.poss_in_rows = [set(j for j in range(10)) for i in range(9)]
        self.poss_in_grids = [set(j for j in range(10)) for i in range(9)]
        self.poss_in_columns = [set(j for j in range(10)) for i in range(9)]
        self.grid_rep = self.repGrids()


    def __str__(self):
        board_string = ''
        for i in range(9):
            if i%3 == 0: board_string += '                     \n'; #to have a horizontal spacer between grids of nine

            for j in range(9):
                if j%3 == 0: board_string += '   ';#to have vertical spacer between grids of nine

                board_string += f" {self.gameboard[i][j]} "#fill in the box with the index of the grid at (row i,column j)

            board_string += '\n'

        return board_string


#     def PossibleByLine(value,rowOrCol): #returns true when a value does not already exist in an inputted row or column numpy.array(slot)
#         return filter(lambda rowOrColVal: rowOrColVal != value,rowOrCol)

    def repGrids(self):
        ret_grids = np.empty((9,9),dtype = object)
        for i in range(3):
            for j in range(3):
                ret_grids[3*i+j] = self.game_board[3*i:3*i+3,3*j:3*j+3].flatten()
        return ret_grids

    def getRows(self):
        for x in range(9):
            row_taken_values = {slot.value for slot in self.game_board[x]}
            self.poss_in_rows[x] -= row_taken_values
            
        
    def getColumns(self):
        for x in range(9):
            column_taken_values = {slot.value for slot in self.game_board[:,x]}
            self.poss_in_columns[x] -= column_taken_values
        
    def getGrids(self):
        for x in range(3):
            for y in range(3):
                flattened = self.game_board[3*x:3*x+3, 3*y:3*y+3].flatten()
                used_nums = {slot.value for slot in flattened}
                self.poss_in_grids[3*x+y] -= used_nums

    def updateBoard(self):
        for i in range(100):
            for row in self.game_board:
                for slot in row:
                    if slot.value == 0:
                        slot.updatePossibleValues(self.poss_in_rows[slot.row], self.poss_in_columns[slot.column], self.poss_in_grids[slot.grid])
                        if slot.value != 0:
                            self.poss_in_rows[slot.row] -= {slot.value}
                            self.poss_in_columns[slot.column] -= {slot.value}
                            self.poss_in_grids[slot.grid] -= {slot.value}
            self.checkSectionUnique(self.game_board)
            self.checkSectionUnique(np.transpose(self.game_board))
            self.checkSectionUnique(self.grid_rep)

    def checkSectionUnique(self, section):
        for i in range(9):
            for num in self.poss_in_rows[i]:
                count = 0
                slot_for_num = None
                for slot in section[i]:
                    if slot.value == 0 and num in slot.possible_values:
                        count += 1
                        slot_for_num = slot
                if count == 1:
                    slot_for_num.value = num
                    slot_for_num.possible_values = {0}                       

            
    # def nextMove(self):
    #     for slot in self.game_board:
    #         if len(slot.possible_values) == 1:
    #             self.updaterowsandgridandcolumn(slot)
    #         elif len(slot.possibleValues) > 1:
    #             slot.updatePossibleValues(row[self.row], column[self.column], grid[self.grid])
            
    #     self.nextMove()
       #    def updateBoard(self):
#        didUpdate = False
 #       for row in self.gameboard:
 #           for slot in row:
 #               if slot.value == 0:
 #                  slot.updatePossibleValues(self.row[slot.row], self.column[slot.column], self.grid[slot.grid])
 #                   if slot.value != 0:
 #                       didUpdate = True
 #                       self.row[slot.row] -= {slot.value}
 #                       self.column[slot.column] -= {slot.value}
#                        self.grid[slot.grid] -= {slot.value}
#        if didUpdate:
 #           self.updateBoard()
 #       elif self.isSolved():
 #           print(self)
 #       else:
 #           self.secondAlgo()

    def secondAlgo(self):
        pass
        #check for zeros in the matrix
        #if there are some zeros we can try part two of our algorithm

        #     if didUpdate == false:
        #     r#un our second algorithim
        # else:
        #     updateBoard()

        #didUpdate = false 2*, we stop our recursion

    def isSolved(self):
        for i in range(9):
            for j in range(9):
                if self.gameboard[i][j] == 0:
                    return False
        return True
                
class Slot:



    def __init__(self, value, x,y):
        self.row = x
        self.column = y
        self.grid = 3 * (x//3) + (y//3)
        self.value = int(value)
        self.possible_values = {1,2,3,4,5,6,7,8,9}
    def __str__(self):
        return str(self.value)

    def getValue(self):
        return self.value

    def getPossibleValues(self):
        return self.possible_values

    
    def updateSlot(self,value):
        self.value = value
        self.possible_values = {0}
    

    def updatePossibleValues(self, row_values, column_values, grid_values):
        self.possible_values = set.intersection(row_values, column_values, grid_values)
        if len(self.possible_values) == 1:
            self.updateSlot(next(iter(self.possible_values)))



#inp_game = "800504013100000600002010570407000905500420000000059460081002000000975182000001000"

inp_game = "000010000035000040008094036600070000000309450000008000009000700000700200403002000"
gameboard = Board(inp_game)

gameboard.getRows()
gameboard.getColumns()
gameboard.getGrids()
gameboard.updateBoard()
print("==========================================")
print(gameboard)
