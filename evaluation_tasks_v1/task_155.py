import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find all instances of color 4 in the grid.
    For each 4, check if it forms an X 4 X pattern (horizontally or vertically).
    Count which color X appears most frequently in these patterns.
    Return a 1x1 grid containing that color.
    '''
    h, w = grid.height, grid.width

    # Count how many times each color appears in X 4 X patterns
    color_counts = {}

    for r in range(h):
        for c in range(w):
            if grid[r][c] == 4:
                # Check horizontal pattern: X 4 X
                if c > 0 and c < w - 1:
                    left = grid[r][c-1]
                    right = grid[r][c+1]
                    if left == right and left != 4 and left != 0:
                        color_counts[left] = color_counts.get(left, 0) + 1

                # Check vertical pattern: X above 4 X below
                if r > 0 and r < h - 1:
                    above = grid[r-1][c]
                    below = grid[r+1][c]
                    if above == below and above != 4 and above != 0:
                        color_counts[above] = color_counts.get(above, 0) + 1

    # Find the color with the highest count
    if color_counts:
        most_frequent_color = max(color_counts, key=color_counts.get)
    else:
        most_frequent_color = 0

    # Return a 1x1 grid with the result
    result = Grid([[most_frequent_color]])
    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("642d658d", solve)
