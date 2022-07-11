import numpy as np
class Board:
    def __init__(self, inp):
        self.game_board = np.empty((9,9),dtype = object)
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

                board_string += f" {self.game_board[i][j]} "#fill in the box with the index of the grid at (row i,column j)

            board_string += '\n'

        return board_string


    def PossibleByLine(slot,rowOrCol): #returns true when a value does not already exist in an inputted row or column numpy.array(slot)
        return filter(lambda rowOrColVal: rowOrColVal != slot.value,rowOrCol)

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
        did_update = False
        for row in self.game_board:
            for slot in row:
                if slot.value == 0:
                    slot.updatePossibleValues(self.poss_in_rows[slot.row], self.poss_in_columns[slot.column], self.poss_in_grids[slot.grid])
                    if slot.value != 0:
                        self.poss_in_rows[slot.row] -= {slot.value}
                        self.poss_in_columns[slot.column] -= {slot.value}
                        self.poss_in_grids[slot.grid] -= {slot.value}
                        did_update = True
        if did_update :
            self.updateBoard()
        elif self.isSolved():
            print(self)    
        else:
            self.secondAlgo()

    def checkSectionUnique(self, section, poss_in_section):
        did_update = False
        for i in range(9):
            for num in poss_in_section[i].copy():
                count = 0
                slot_for_num = None
                for slot in section[i]:
                    if slot.value == 0 and num in slot.possible_values:
                        count += 1
                        slot_for_num = slot
                if count == 1:
                    slot_for_num.updateSlot(num)
                    self.poss_in_rows[slot_for_num.row] -= {num}
                    self.poss_in_columns[slot_for_num.column] -= {num}
                    self.poss_in_grids[slot_for_num.grid] -= {num}
                    did_update = True               
        if did_update:
            self.updateBoard()


    def secondAlgo(self):
        self.checkSectionUnique(self.game_board, self.poss_in_rows)
        self.checkSectionUnique(np.transpose(self.game_board), self.poss_in_columns)
        self.checkSectionUnique(self.grid_rep, self.poss_in_grids)

    # def thirdAlgo:
    #     short list length possible = 2
    #     shortlist[0]: {1, 5}
    #     updateBoard();

    def isSolvable(self):

        return True

    def isSolved(self):
        for i in range(9):
            for j in range(9):
                if self.game_board[i][j].value == 0:
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
    
    def updateSlot(self,value):
        self.value = value
        self.possible_values = {0}
    

    def updatePossibleValues(self, row_values, column_values, grid_values):
        self.possible_values = set.intersection(row_values, column_values, grid_values)
        if len(self.possible_values) == 1:
            self.updateSlot(next(iter(self.possible_values)))


import time
#inp_game = "800504013100000600002010570407000905500420000000059460081002000000975182000001000"
inp_game = "100097000000030008609500003000000640001000000048079005930010006000000000004700530"
#inp_game = "000010000035000040008094036600070000000309450000008000009000700000700200403002000"
start = time.time()
game_board = Board(inp_game)
print(game_board)
game_board.getRows()
game_board.getColumns()
game_board.getGrids()
game_board.updateBoard()

print("==========================================")
print(game_board)
end = time.time()
print(end-start)
