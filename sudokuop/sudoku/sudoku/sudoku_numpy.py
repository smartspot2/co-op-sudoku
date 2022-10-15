import numpy as np

class Sudoku(object):
    N = 9
    def __init__(self):
        self.grid = np.ones((self.N, self.N, self.N))
        self.views = []
    
    def get_row(self, i):
        return self.grid[i, :, :]
    
    def get_col(self, i):
        return self.grid[:, i, :]
    
    def remove(self, row, col, candidates):
        self.grid[row, col, candidates - 1] = 0
    
    def set(self, row, col, n):
        self.grid[row, col] *= 0
        self.grid[row, col, n] = 1
