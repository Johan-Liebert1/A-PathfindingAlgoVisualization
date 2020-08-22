import pygame
from math import sqrt
from colors import colors
from node import make_grid


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

def show_steps(grid, endNode, finalSol = False):
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

            if grid[row][col].isPath and finalSol:
                color = colors['blue']

            if grid[row][col] == endNode:
                color = colors['end_node']

            pygame.draw.rect(
                window, 
                color, 
                (
                    row * cell_height + 1, 
                    col * cell_width + 1,   
                    cell_width - 1, 
                    cell_height - 1
                )
            )
    
    pygame.display.update()


# HScore function

def getHScore(node, endNode):
    return sqrt(abs(node.i - endNode.i)**2 + abs(node.j - endNode.j)**2)


# A* PATHFINDING ALGORITHM

def aStar(start_node, end_node):
    # node.f = node.g + node.h
    # node.g = distance of current node from the starting node
    # node.h = distance of current node from the end node

    start_node.g = 0
    start_node.h = getHScore(start_node, end_node)
    start_node.f = start_node.g + start_node.h
    open_set = [start_node]
    closed_set = []

    while True:
        if len(open_set) < 1:
            print('No Solutions Found')
            break

        current_node = open_set[0]

        for node in open_set:
            if node.f < current_node.f:
                current_node = node
                current_node.isOpen = True

        # print(f'current_node = {current_node.i, current_node.j}', end = " ")

        current_node.isPath = True

        if current_node == end_node:
            show_steps(main_grid, end_node, finalSol = True)

            return

        current_node.isOpen = False

        open_set.remove(current_node)
        closed_set.append(current_node)

        for neighbor in current_node.neighbors:
            # assuming 1 as the distance btw two neighbouring points that aren't diagonally
            # neighbors

            # need to add 1.14 if neighbor is diagonal. add propery to node class to check if neighbor is diagonal

            if neighbor in closed_set:
                continue

            tempG = current_node.g + getHScore(current_node, neighbor)

            if neighbor not in open_set and not neighbor.isWall:
                open_set.append(neighbor)
                neighbor.isOpen = True

            if tempG >= neighbor.g:
                continue # there is not a better path
            

            neighbor.previous = current_node
            neighbor.isPath = True
            neighbor.g = tempG
            neighbor.h = getHScore(neighbor, end_node)
            neighbor.f = neighbor.g + neighbor.h

        show_steps(main_grid, end_node)


aStar(main_grid[0][0], main_grid[10][10])

# MAIN LOOP

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
