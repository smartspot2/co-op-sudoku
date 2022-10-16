import numpy as np
from numpy.random import default_rng
import itertools

from pyparsing import col

class Board(object):
    """
    Stores the state of the board in a ROW x COL x CANDIDATE grid
    """
    N = 9
    def __init__(self):
        self.grid = np.ones((self.N, self.N, self.N))
    
    def get_row(self, i):
        return self.grid[i, :, :]
    
    def get_row_indices(self, i):
        return [(i, j) for j in range(self.N)]
        
    def get_col(self, j):
        return self.grid[:, j, :]
    
    def get_col_indices(self, j):
        return [(i, j) for i in range(self.N)]
    
    def get_block(self, i, j):
        i = 3 * (i // 3)
        j = 3 * (j // 3)
        return self.grid[i:i+3, j:j+3, :]
    
    def get_block_indices(self, i, j):
        i = 3 * (i // 3)
        j = 3 * (j // 3)
        return list(itertools.product([i, i+1, i+2], [j, j+1, j+2]))
    
    def get_neighbor_indices(self, i, j):
        row_neighbors = self.get_row_indices(i)
        col_neighbors = self.get_col_indices(j)
        block_neighbors = self.get_block_indices(i, j)

        neighbors = set(row_neighbors + col_neighbors + block_neighbors)
        neighbors.remove((i, j))

        return list(neighbors)
    
    def remove_from_cell(self, row, col, candidates):
        self.grid[row, col, candidates] = 0

    def remove_from_cells(self, indices, candidates):
        for row, col in indices:
            self.remove_from_cell(row, col, candidates)

    def remove_from_row(self, row, candidates):
        self.grid[row, :, candidates] = 0
    
    def remove_from_col(self, col, candidates):
        self.grid[:, col, candidates] = 0
    
    def remove_from_block(self, i, j, candidates):
        block = self.get_block(i, j)
        block[:, :, candidates] = 0
    
    def cell_is_single(self, row, col):
        return self.grid[row, col].sum() == 1

    def set_cell(self, row, col, n):
        self.grid[row, col] *= 0
        self.grid[row, col, n] = 1
        assert self.cell_is_single(row, col)
    
    def get_cell(self, row, col):
        assert self.cell_is_single(row, col)
        return np.where(self.grid[row, col] == 1)[0][0]

    def copy(self):
        copy = Board()
        copy.grid = self.grid.copy()
        return copy
    
    def __str__(self):
        return str(self.grid)

class Game(object):
    N = 9
    def __init__(self, num_players=2):
        self.num_players = num_players
        self.board = Board()
        self._reset_views()
    
    def _reset_views(self):
        self.views = np.zeros((self.num_players, self.N, self.N))

    def generate_views(self, overlap=2, replace=True):
        self._reset_views()
        rng = default_rng()

        for i, j in itertools.product(range(self.N), range(self.N)):
            view_idxs = rng.choice(self.num_players, size=overlap, replace=replace)
            self.views[view_idxs, i, j] = 1

        # every square must be seen
        assert (np.sum(self.views, axis=0) > 0).all()
    
    def generate_toy_view(self):
        assert self.num_players == 2
        self._reset_views()
        self.views[0, :6, :9] = 1
        self.views[1, 3:, :9] = 1


class Solver(object):
    N = 9
    def __init__(self, game: Game):
        self.board = game.board.copy()
        self.views = game.views.copy()
    
    def solve(self, view):
        for i, j in itertools.product(range(self.N), range(self.N)):
            if view[i, j] and self.board.cell_is_single(i, j):
                index = self.board.get_cell(i, j)
                neighbors = self.board.get_neighbor_indices(i, j)
                self.board.remove_from_cells(neighbors, index)

