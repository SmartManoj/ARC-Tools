import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern analysis for task 1e81d6f9:
    1. Each grid has a cross-shaped marker made of 5's in the top-left corner
       - Vertical line: column 3, rows 0-3
       - Horizontal line: row 3, columns 0-3
    2. Inside the cross region (rows 0-2, columns 0-2), there's a marker color at position [1,1]
    3. Remove all instances of that marker color from outside the cross region

    The cross region is defined as rows 0-3 and columns 0-3 (the area bounded by the 5's).
    '''
    # Get grid dimensions
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Create a copy of the grid data
    output_data = [[grid[r][c] for c in range(width)] for r in range(height)]

    # Find the marker color at position [1, 1]
    marker_color = grid[1][1]

    # If marker_color is 0 or 5, there's nothing special to remove
    if marker_color == 0 or marker_color == 5:
        return Grid(output_data)

    # Remove all instances of marker_color outside the cross region
    # The cross region is rows 0-3 and columns 0-3
    for r in range(height):
        for c in range(width):
            # If we're outside the cross region and the cell has the marker color
            if (r > 3 or c > 3) and output_data[r][c] == marker_color:
                output_data[r][c] = 0

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("1e81d6f9", solve)
