import time
import itertools

import numpy as np
from numpy.random import default_rng

# should in theory work for arbitrary sized sudoku boards, but slow
SIZE = 16
BLOCK_SIZE = 4

INDICES = list(itertools.product(range(SIZE), range(SIZE)))

class FlatBoard(object):
    """
    Stores the state of the board in a ROW x COL grid
    """
    def __init__(self):
        self.grid = np.zeros((SIZE, SIZE))
    
    def __str__(self):
        return str(self.grid)

    def __repr__(self):
        return str(self.grid)

    def __hash__(self):
        return hash(str(self.grid))
    
    def __eq__(self, other):
        return (self.grid == other.grid).all()


class Board(object):
    """
    Stores the state of the board in a ROW x COL x CANDIDATE grid
    """
    def __init__(self):
        self.grid = np.ones((SIZE, SIZE, SIZE))
    
    def get_row(self, i):
        return self.grid[i, :, :]
    
    def get_row_indices(self, i):
        return [(i, j) for j in range(SIZE)]
        
    def get_col(self, j):
        return self.grid[:, j, :]
    
    def get_col_indices(self, j):
        return [(i, j) for i in range(SIZE)]
    
    def get_block(self, i, j):
        i = BLOCK_SIZE * (i // BLOCK_SIZE)
        j = BLOCK_SIZE * (j // BLOCK_SIZE)
        return self.grid[i:i+BLOCK_SIZE, j:j+BLOCK_SIZE, :]
    
    def get_block_indices(self, i, j):
        i = BLOCK_SIZE * (i // BLOCK_SIZE)
        j = BLOCK_SIZE * (j // BLOCK_SIZE)
        return list(itertools.product(range(i, i+BLOCK_SIZE), range(j, j+BLOCK_SIZE)))
    
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

    def reset_cell(self, row, col):
        self.grid[row, col] = np.ones(SIZE)

    def set_cell(self, row, col, n):
        self.grid[row, col] *= 0
        self.grid[row, col, n] = 1
        assert self.cell_is_single(row, col)
    
    def get_cell_candidates(self, row, col):
        return np.where(self.grid[row, col] == 1)[0]

    def get_cell_value(self, row, col):
        assert self.cell_is_single(row, col)
        return np.where(self.grid[row, col] == 1)[0][0]

    def flatten(self):
        flat_grid = [[0] * SIZE for _ in range(SIZE)]
        for i, j in INDICES:
            if self.cell_is_single(i, j):
                flat_grid[i][j] = self.get_cell_value(i, j) + 1
        flat_board = FlatBoard()
        flat_board.grid = np.array(flat_grid)
        return flat_board

    def copy(self):
        copy = Board()
        copy.grid = self.grid.copy()
        return copy
    
    def __str__(self):
        return str(self.flatten())
    
    def __hash__(self):
        return hash(str(self.grid))
    
    def __eq__(self, other):
        return (self.grid == other.grid).all()


class Game(object):
    def __init__(self, num_players=2):
        self.num_players = num_players
        self.board = Board()
        self._reset_views()
    
    def _reset_views(self):
        self.views = np.zeros((self.num_players, SIZE, SIZE))

    def generate_views(self, overlap=2, replace=True):
        self._reset_views()
        rng = default_rng()

        for i, j in INDICES:
            view_idxs = rng.choice(self.num_players, size=overlap, replace=replace)
            self.views[view_idxs, i, j] = 1

        # every square must be seen
        assert (np.sum(self.views, axis=0) > 0).all()
    
    def generate_toy_view(self):
        assert SIZE == 9 and BLOCK_SIZE == 3
        assert self.num_players == 2
        self._reset_views()
        self.views[0, :6, :9] = 1
        self.views[1, 3:, :9] = 1
    
    def generate_toy_board(self):
        assert SIZE == 9 and BLOCK_SIZE == 3
        from examples import solvable_1, solvable_2, unsolvable_1, unsolvable_2
        self.board = Board()
        for idx, n in enumerate(unsolvable_1['values']):
            i = idx // SIZE
            j = idx % SIZE
            if n > 0:
                self.board.set_cell(i, j, n - 1)

class Solver(object):
    def __init__(self, game: Game):
        self.board = game.board.copy()
        self.views = game.views.copy()
        self.solution = None
    
    def solved(self):
        def one_through_N(subset):
            subset = subset.reshape((-1, SIZE))
            return (subset.sum(axis=0) == 1).all() and \
                   (subset.sum(axis=1) == 1).all()

        if not self.board.is_filled():
            return False
        
        for i, j in INDICES:
            row = self.board.get_row(i)
            col = self.board.get_col(j)
            block = self.board.get_block(i, j)

            if not one_through_N(row):
                return False
            if not one_through_N(col):
                return False
            if not one_through_N(block):
                return False
        return True
    
    def remove_matching_candidates_in_view(self, i, j, view):
        if view[i, j] and self.board.cell_is_single(i, j):
            index = self.board.get_cell_value(i, j)
            neighbors = self.board.get_neighbor_indices(i, j)
            neighbors = [(x, y) for x, y in neighbors if view[x, y]]
            num_removed = self.board.remove_from_cells(neighbors, index)
            return num_removed
        return 0
    
    def iterative_solve(self):
        self.solution = []
        attempts = 0
        modified = True
        while modified and attempts < 100000:
            modified = False
            for view in self.views:
                for i, j in INDICES:
                    num_removed = self.remove_matching_candidates_in_view(i, j, view)
                    if num_removed > 0:
                        modified = True
                        self.solution.append((i, j))
            attempts += 1
        return self.solved()
    
    def backtrack_solve(self, i=0, j=0):
        next_i = i + (j + 1) // SIZE
        next_j = (j + 1) % SIZE

        if i >= SIZE:
            return True
        if self.board.cell_is_single(i, j):
            return self.backtrack_solve(next_i, next_j)

        candidates = list(range(SIZE))
        np.random.shuffle(candidates)
        for candidate in candidates:
            neighbors = self.board.get_neighbor_indices(i, j)
            valid = True
            for x, y in neighbors:
                if self.board.cell_is_single(x, y):
                    if self.board.get_cell_value(x, y) == candidate:
                        valid = False
            if valid:
                self.board.set_cell(i, j, candidate)
                solved = self.backtrack_solve(next_i, next_j)
                if solved:
                    return True
                self.board.reset_cell(i, j)
        return False
    
    def generate_greedy(self, search_time_limit=30):
        start_time = time.time()

        self.board = Board()
        self.backtrack_solve()

        search_start_time = time.time()

        solvable_boards = []
        solvable_boards.append(self.board.copy())

        order = list(INDICES)
        np.random.shuffle(order)

        for i, j in order:
            if self.board.cell_is_single(i, j):
                prereset = self.board.copy()
                self.board.reset_cell(i, j)
                postreset = self.board.copy()

                if self.iterative_solve():
                    solvable_boards.append(postreset.copy())
                    self.board = postreset
                else:
                    self.board = prereset
            
            if time.time() - search_start_time > search_time_limit:
                print('search time limit exceeded')
                break
        
        print(f'backtrack time: {search_start_time - start_time:.2f} s')
        print(f'search time: {time.time() - search_start_time:.2f} s')
        return solvable_boards
