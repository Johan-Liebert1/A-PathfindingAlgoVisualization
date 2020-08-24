import pygame
from math import sqrt
from colors import colors
from node import make_grid
import time

# making the grid
grid_len = 20
main_grid = make_grid(grid_len)
path = [] # to reconstruct the optimal path


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

def show_steps(grid, sNode, endNode, finalSol = False):
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
            
            if grid[row][col] == sNode:
                color = colors['start_node']

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


def colorFinalPath(grid):
    print(f'path = {path}')
    cell_width = WIN_WIDTH // grid_len
    cell_height = WIN_HEIGHT // grid_len

    for row in range(grid_len):
        for col in range(grid_len):

            if grid[row][col] in path:
                print('coloring blue')
                color = colors['blue']

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

    if start_node.isWall:
        print("The start node is a wall")
        return

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

        if current_node == end_node:
            temp = end_node
            path.append(temp)

            while temp.previous is not None:
                path.append(temp.previous)
                temp = temp.previous

            print("DONE")
            colorFinalPath(main_grid)
            break

        # current_node.isPath = True
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
                neighbor.g = tempG
                open_set.append(neighbor)
                neighbor.isOpen = True
                neighbor.previous = current_node

            if tempG >= neighbor.g:
                continue # there is no better path
            
            # neighbor was found in the open set, so we check if we can get to it in 
            # a better way as tempG is now less than neighbor.g
            neighbor.previous = current_node
            # neighbor.isPath = True
            neighbor.g = tempG
            neighbor.h = getHScore(neighbor, end_node)
            neighbor.f = neighbor.g + neighbor.h

        show_steps(main_grid, start_node, end_node)


aStar(main_grid[0][0], main_grid[10][10])

# MAIN LOOP

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
