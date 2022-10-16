import numpy as np
import itertools


class Board(object):
    N = 9
    def __init__(self):
        self.grid = np.ones((self.N, self.N, self.N))
    
    def get_row(self, i):
        return self.grid[i, :, :]
    
    def get_col(self, i):
        return self.grid[:, i, :]
    
    def get_square(self, i, j):
        assert 0 <= i < 3 and 0 <= i < 3
        return self.grid[i:i+3, j:j+3, :]
    
    def remove(self, row, col, candidates):
        self.grid[row, col, candidates] = 0
    
    def set(self, row, col, n):
        self.grid[row, col] *= 0
        self.grid[row, col, n] = 1


class Sudoku(object):
    def __init__(self, num_players=2):
        self.board = Board()
        self.num_players = num_players
        self.views = None

    def generate_views(self, n, overlap=2, replace=True):
        from numpy.random import default_rng

        rng = default_rng()
        self.views = np.zeros((n, self.N, self.N))

        # every square must be seen
        for i, j in itertools.product(range(self.N), range(self.N)):
            view_idxs = rng.choice(n, size=overlap, replace=replace)
            self.views[view_idxs, i, j] = 1

        assert (np.sum(self.views, axis=0) > 0).all()
    
    def _generate_toy_view(self):
        self.views = np.ones(())