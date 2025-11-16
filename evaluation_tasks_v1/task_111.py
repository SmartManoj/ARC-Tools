import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Place copies of the 3x3 input grid in a 9x9 output grid
    based on the minority color positions.

    1. Find the color that appears least frequently (minority color)
    2. Create a 9x9 output grid filled with zeros
    3. For each position (i,j) in the input where the cell has the minority color,
       place a copy of the entire input at position (i*3, j*3) in the output
    '''
    # Count occurrences of each color
    color_counts = {}
    for row in grid:
        for cell in row:
            color_counts[cell] = color_counts.get(cell, 0) + 1

    # Find the minority color (least frequent)
    minority_color = min(color_counts.keys(), key=lambda c: color_counts[c])

    # Create 9x9 output grid filled with zeros
    output = [[0 for _ in range(9)] for _ in range(9)]

    # For each cell in the 3x3 input
    for i in range(3):
        for j in range(3):
            # If this cell has the minority color
            if grid[i][j] == minority_color:
                # Place a copy of the entire input at position (i*3, j*3)
                for di in range(3):
                    for dj in range(3):
                        output[i*3 + di][j*3 + dj] = grid[di][dj]

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("48f8583b", solve)
