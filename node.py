class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isWall = False
        self.f = 0
        self.g = 0
        self.h = 0


def make_grid(length):
    main_grid = []
    for i in range(length):
        lst = []
        for j in range(length):
            lst.append(Node(i, j))

        main_grid.append(lst)

    return main_grid