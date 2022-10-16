import numpy as np
from numpy.random import default_rng
import itertools

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
        num_removed = self.grid[row, col, candidates].sum()
        self.grid[row, col, candidates] = 0
        return num_removed

    def remove_from_cells(self, indices, candidates):
        num_removed = 0
        for row, col in indices:
            num_removed += self.remove_from_cell(row, col, candidates)
        return num_removed

    def remove_from_row(self, row, candidates):
        self.grid[row, :, candidates] = 0
    
    def remove_from_col(self, col, candidates):
        self.grid[:, col, candidates] = 0
    
    def remove_from_block(self, i, j, candidates):
        block = self.get_block(i, j)
        block[:, :, candidates] = 0
    
    def cell_is_single(self, row, col):
        return self.grid[row, col].sum() == 1
    
    def is_filled(self):
        return (self.grid.sum(axis=2) == 1).all()

    def set_cell(self, row, col, n):
        self.grid[row, col] *= 0
        self.grid[row, col, n] = 1
        assert self.cell_is_single(row, col)
    
    def get_cell(self, row, col):
        assert self.cell_is_single(row, col)
        return np.where(self.grid[row, col] == 1)[0][0]

    def flatten(self):
        flat_grid = [[0] * self.N for _ in range(self.N)]
        for i, j in itertools.product(range(self.N), range(self.N)):
            if self.cell_is_single(i, j):
                flat_grid[i][j] = self.get_cell(i, j) + 1
        return flat_grid

    def copy(self):
        copy = Board()
        copy.grid = self.grid.copy()
        return copy
    
    def __str__(self):
        return str(self.flatten())


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
    
    def generate_toy_board(self):
        from examples import solvable_1, unsolvable_1
        self.board = Board()
        for idx, n in enumerate(solvable_1['values']):
            i = idx // self.N
            j = idx % self.N
            if n > 0:
                self.board.set_cell(i, j, n - 1)

class Solver(object):
    N = 9
    def __init__(self, game: Game):
        self.board = game.board.copy()
        self.views = game.views.copy()
    
    def solved(self):
        def one_through_nine(subset):
            subset = subset.reshape((-1, self.N))
            return (subset.sum(axis=0) == 1).all() and \
                   (subset.sum(axis=1) == 1).all()

        if not self.board.is_filled():
            return False
        
        for i, j in itertools.product(range(self.N), range(self.N)):
            row = self.board.get_row(i)
            col = self.board.get_col(j)
            block = self.board.get_block(i, j)

            if not one_through_nine(row):
                return False
            if not one_through_nine(col):
                return False
            if not one_through_nine(block):
                return False
        return True
    
    def iterative_solve(self):
        attempts = 0
        modified = True
        while modified and attempts < 100000:
            modified = False
            for view in self.views:
                for i, j in itertools.product(range(self.N), range(self.N)):
                    if view[i, j] and self.board.cell_is_single(i, j):
                        index = self.board.get_cell(i, j)
                        neighbors = self.board.get_neighbor_indices(i, j)
                        num_removed = self.board.remove_from_cells(neighbors, index)
                        if num_removed > 0:
                            modified = True
            attempts += 1
        return self.solved()

