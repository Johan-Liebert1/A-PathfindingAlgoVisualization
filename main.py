import pygame

from colors import colors
from node import make_grid

grid_len = 20

main_grid = make_grid(grid_len)

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

# MAIN LOOP

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False