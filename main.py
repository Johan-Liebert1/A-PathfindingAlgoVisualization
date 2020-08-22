import pygame

from colors import colors
from node import make_grid

path = []

# making the grid
grid_len = 20
main_grid = make_grid(grid_len)

# pygame config
pygame.init()
WIN_WIDTH = 600
WIN_HEIGHT = 600
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
window.fill(colors['white'])
pygame.display.flip()


def display_grid(grid):
    
    cell_width = WIN_WIDTH // grid_len
    cell_height = WIN_HEIGHT // grid_len

    for i in range(grid_len):
        pygame.draw.line(window, colors['black'], (0, i * cell_height), (WIN_WIDTH, i * cell_height))

        for j in range(grid_len):
            pygame.draw.line(window, colors['black'], (j * cell_width, 0), (j * cell_width, WIN_HEIGHT))
    
    pygame.display.update()

display_grid(main_grid)

def show_steps(grid, endNode):
    cell_width = WIN_WIDTH // grid_len
    cell_height = WIN_HEIGHT // grid_len

    for row in range(grid_len):
        for col in range(grid_len):

            
            if not grid[row][col].isWall:
                color = colors['green'] if grid[row][col].isOpen else colors['red']

            if grid[row][col].isOpen is None:
                color = colors['white']

            if grid[row][col].isWall:
                color = colors['black']

            if grid[row][col] == endNode:
                color = colors['end_node']

            pygame.draw.rect(
                window, 
                color, 
                (
                    row * cell_height + 2.5, 
                    col * cell_width + 2.5,   
                    cell_width - 5, 
                    cell_height - 5
                )
            )
    
    pygame.display.update()

# def see_neighbors():
#     for i in range(len(main_grid)):
#             for j in range(len(main_grid[i])):
#                 for neighbor in main_grid[i][j].neighbors:
#                     print(f'neighbor for {i}{j} = {neighbor.i}, {neighbor.j}', end = ' ')
#                print("")

def getHScore(node, endNode):
    return abs(node.i - endNode.i) + abs(node.j - endNode.j)


# A* PATHFINDING ALGORITHM

def aStar(start_node, end_node):
    # node.f = node.g + node.h
    # node.g = distance of current node from the starting node
    # node.h = distance of current node from the end node

    # closed_set = []
    start_node.g = 0
    start_node.f = start_node.g + getHScore(start_node, end_node)
    open_set = [start_node]


    while len(open_set) > 0:
        # print(open_set)
        # for i in range(len(main_grid)):
        #     for j in range(len(main_grid[i])):

        current_node = open_set[0]

        for node in open_set:
            if node.f < current_node.f:
                current_node = node
                current_node.isOpen = True

        print(f'current_node = {current_node.i, current_node.j}', end = " ")

        current_node.isPath = True

        if current_node == end_node:
            return

        current_node.isOpen = False

        open_set.remove(current_node)
        

        for neighbor in current_node.neighbors:
            # assuming 1 as the distance btw tow neighbouing poitns
            # print(f'neighbor = {neighbor}')

            tempG = current_node.g + 1

            if tempG < neighbor.g:
                neighbor.g = tempG
                neighbor.h = getHScore(neighbor, end_node)
                neighbor.f = neighbor.g + neighbor.h

            if neighbor not in open_set and not neighbor.isWall:
                open_set.append(neighbor)
                neighbor.isOpen = True

        show_steps(main_grid, end_node)



aStar(main_grid[0][0], main_grid[10][10])
# see_neighbors()

# MAIN LOOP

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    