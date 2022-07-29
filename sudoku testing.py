import numpy as np
import time
# This is the class board. It has attributes such as inp to determine the game to be played. It's required to be initialized.
class Board:
    def __init__(self, inp):
        self.inp = inp
        self.game_board = np.empty((9,9),dtype = object)
        for x in range(9):
            for y in range(9):

                self.game_board[x][y] = Slot(inp[9*x + y], x, y)
                if int(inp[9*x+y]) != 0:
                    self.game_board[x][y].possible_values = {0}
        self.poss_in_rows = [set(j for j in range(10)) for i in range(9)]
        self.poss_in_grids = [set(j for j in range(10)) for i in range(9)]
        self.poss_in_columns = [set(j for j in range(10)) for i in range(9)]
        self.grid_rep = self.repGrids()
        self.getRows()
        self.getColumns()
        self.getGrids()

    def __str__(self):
        board_string = '\n=========================================\n'
        for i in range(9):
            if i%3 == 0: board_string += '                     \n'; #to have a horizontal spacer between grids of nine

            for j in range(9):
                if j%3 == 0: board_string += '   ';#to have vertical spacer between grids of nine

                board_string += f" {self.game_board[i][j]} "#fill in the box with the index of the grid at (row i,column j)

            board_string += '\n'
        return board_string

    def convertArray(self):
        ret_array = np.zeros((9,9))
        for i in range(9):
            for j in range(9):
                ret_array[i,j] = self.game_board[i][j].value
        return ret_array
        
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


# Methods to update each slot accessed through the board which contains those slots
    def updateBoard(self):
        did_update = False
        for row in self.game_board:
            for slot in row:
                if slot.value == 0:
                    slot.updatePossibleValues(self.poss_in_rows[slot.row], self.poss_in_columns[slot.column], self.poss_in_grids[slot.grid])
                    if len(slot.possible_values) == 1:
                        self.boardUpdateSlot(slot, next(iter(slot.possible_values)))
                        did_update = True
        if self.isSolved():
            return
        elif did_update:  
            self.updateBoard()
        else:  
            self.thirdAlgo()
            
    def secondAlgo(self):
        did_update = self.checkSectionUnique(self.game_board, self.poss_in_rows)
        did_update += self.checkSectionUnique(np.transpose(self.game_board), self.poss_in_columns)
        did_update += self.checkSectionUnique(self.grid_rep, self.poss_in_grids)
        if self.isSolved():
            return
        elif did_update:
            self.updateBoard()
        else:
            self.thirdAlgo()

    def thirdAlgo(self):
        x, y = self.findLeastPoss()
        init_board = self.convertArray()
        if x == None:
            did_finish = self.bruteForce(init_board)
            if did_finish:
                return
            else:
                print("This board is unsolvable.")
        else:
            least_choices_slot = self.game_board[x][y]
            possibilities = list(least_choices_slot.possible_values)
            poss1 = possibilities[0]
            poss2 = possibilities[1]
            init_board[x,y] = poss1
            did_finish = self.bruteForce(init_board)
            if did_finish:
                self.boardUpdateSlot(self.game_board[x,y], poss1)
                return
            else:
                self.boardUpdateSlot(self.game_board[x,y], poss2)
                self.updateBoard()

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
                    self.boardUpdateSlot(slot_for_num, num)
                    did_update = True               
        return did_update

    def boardUpdateSlot(self, slot, value):
        slot.updateSlot(value)
        self.poss_in_rows[slot.row] -= {value}
        self.poss_in_columns[slot.column] -= {value}
        self.poss_in_grids[slot.grid] -= {value}


    def isSolved(self):
        for i in range(9):
            for j in range(9):
                if self.game_board[i][j].value == 0:
                    return False
        return True
    
    def findLeastPoss(self):
        for i in range(9):
            for j in range(9):
                if len(self.game_board[i][j].possible_values) == 2:
                    return i, j
        return None, None

    def bruteForce(self, test_board):
        temp_board = test_board.copy()
        next_x, next_y = self.whereEmpty(temp_board)
        if next_x == -1:
            return True
        else:
            for num in range(1,10):
                if self.allowed(temp_board, next_x, next_y, num):
                    temp_board[next_x, next_y] = num
                    if self.bruteForce(temp_board):
                        self.game_board[next_x, next_y].updateSlot(num)
                        return True
                        break
            else:
                return False  

    def allowed(self, board, x, y, num):
        return num not in board[x] and num not in np.transpose(board)[y] and num not in board[3*(x//3):3*(x//3)+3, 3*(y//3):3*(y//3)+3]

    def whereEmpty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i,j
        return -1, -1

# Each slot in the Sudoku Puzzle keeps track of its row, column, and grid for easy reference. We utilize sets because each row, column, or grid can have unique values
class Slot:
    def __init__(self, value, x,y):
        self.row = x
        self.column = y
        self.grid = 3 * (x//3) + (y//3)
        self.value = int(value)
        self.possible_values = {}
        
    def __str__(self):
        return str(self.value)
    
    def updateSlot(self,value):
        self.value = value
        self.possible_values = {0}
# Here is how possible values are found
    def updatePossibleValues(self, row_values, column_values, grid_values):
        self.possible_values = set.intersection(row_values, column_values, grid_values)

# Take your pick at one of our games, or submit your own
def main():
    easy          = "800020910234510007710080054600100305185000720040602800068000400000000162000407530"
    medium        = "300007086005003000000005320940102050200090700850004000089000007070040000034801900"
    hard          = "000500900050020001300609000070180002105000087008004000004750000030208050000406020"
    expert        = "000500000005002940006000070000050020007004100800390000403000006000400007080060002"
    evil          = "080010000000000020006800045004100086000000700300009000400030057007000100000500200"
    devils_sudoku = "800000000003600000070090200050007000000045700000100030001000068008500010090000400" #quote, 'the HARDEST SUDOKU PUZZLE EVER' solves in average of 3.7 seconds
    
    while True:
        try:
            inp = int(input("1: easy\n2: medium\n3: hard\n4: expert\n5: evil \n6: 'hardest sudoku puzzle ever' "))
            assert(0 < inp < 7)
            break
        except:
            print("Invalid number, enter another one.")

    if inp == 1:
        inp_game = easy
    elif inp == 2:
        inp_game = medium
    elif inp == 3:
        inp_game = hard
    elif inp == 4:
        inp_game = expert
    elif inp == 5:
        inp_game = evil
    elif inp == 6:
        inp_game = devils_sudoku    
    
    assert(len(inp_game) == 81)
    game_board = Board(inp_game)
    print(game_board)

    t0 = time.time()
    game_board.updateBoard()
    t1 = time.time()
    total = t1-t0

    print(game_board)
    print("Total time: " + str(total))
    # Thank you for watching
if __name__ == "__main__":
    main()
