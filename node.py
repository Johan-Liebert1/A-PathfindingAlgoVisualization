class Node():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.isWall = False
        self.isOpen = None
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []

    
    def add_neighbors(self, grid):
        i = self.i
        j = self.j

        if i > 0:
            self.neighbors.append(grid[i - 1][j])

        if i < len(grid) - 1:
            self.neighbors.append(grid[i + 1][j])


        if j > 0:
            self.neighbors.append(grid[i][j - 1])

        if j < len(grid) - 1:
            self.neighbors.append(grid[i][j + 1])



def make_grid(length):
    main_grid = []
    for i in range(length):
        lst = []
        for j in range(length):
            node = Node(i, j)

            lst.append(node)

        main_grid.append(lst)


    for i in range(length):
        for j in range(length):
            main_grid[i][j].add_neighbors(main_grid)

    return main_grid

