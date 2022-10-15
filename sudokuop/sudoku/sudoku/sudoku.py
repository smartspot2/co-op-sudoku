class Square(object):
    """
    Contains a set of possible candidates 1 through 9 inclusive
    """
    N = 9
    def __init__(self, id):
        self.id = id
        self.reset()

    def remove(self, n):
        self.candidates.remove(n)

    def reset(self):
        self.candidates = set(range(1, Square.N + 1))

    def set(self, n):
        self.candidates = set([n])

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

class Sudoku(object):
    N = 9
    def __init__(self):
        self.grid = [Square(id) for id in range(self.N * self.N)]
        self.views = []
        self.cols = [self.grid[i::self.N] for i in range(self.N)]
        self.rows = [self.grid[i:i+self.N] for i in range(0, self.N * self.N, self.N)]
        self.squares = [self.grid[i:i+3] + self.grid[i+self.N:i+self.N+3] + self.grid[i+2*self.N:i+2*self.N+3]
                        for i in [0, 3, 6, 27, 30, 33, 54, 57, 60]]
    
    