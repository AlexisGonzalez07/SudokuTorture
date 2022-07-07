
import numpy as np


class Board:
    def __init__(self, inp):
        self.game_board = np.zeros((9,9),dtype = int)
        for x in range(9):
            for y in range(9):
                self.game_board[x][y] = inp[9*x + y]
    def __str__(self):
        boardString = ''
        for i in range(9):
            if i%3 == 0: boardString += '                     \n'; #to have a horizontal spacer between grids of nine

            for j in range(9):
                if j%3 == 0: boardString += '   ';#to have vertical spacer between grids of nine

                boardString += f" {self.game_board[i][j]} "#fill in the box with the index of the grid at (row i,column j)

            boardString += '\n'

        return boardString



inp_game = "530070000600195000098000060800060003400803001700020006060000280000419005000080079" #whatever the hardcoded board will be
gameboard = Board(inp_game)
print(gameboard)