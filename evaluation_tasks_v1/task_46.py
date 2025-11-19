import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern Analysis:
    1. Find the gray (5) rectangle in the input
    2. Find all colored markers (non-0, non-5) around/on the rectangle
    3. Group markers by color
    4. For each color group:
       - Find the bounding box (min/max row and col) of all markers of that color
       - Fill the intersection of this bounding box with the gray rectangle

    The markers define rectangular regions to fill within the gray rectangle.
    '''
    # Find the bounding box of the gray rectangle
    min_r = min_c = float('inf')
    max_r = max_c = -1

    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] == 5:  # Gray color
                min_r = min(min_r, r)
                max_r = max(max_r, r)
                min_c = min(min_c, c)
                max_c = max(max_c, c)

    # Find all markers (non-0, non-5 pixels) and group by color
    markers_by_color = {}
    for r in range(grid.height):
        for c in range(grid.width):
            val = grid[r][c]
            if val != 0 and val != 5:
                if val not in markers_by_color:
                    markers_by_color[val] = []
                markers_by_color[val].append((r, c))

    # Create output grid, starting with the input
    output_grid = [[grid[r][c] for c in range(grid.width)] for r in range(grid.height)]

    # For each color group, find its bounding box and fill the region
    for color, markers in markers_by_color.items():
        # Find bounding box of markers
        marker_min_r = min(r for r, c in markers)
        marker_max_r = max(r for r, c in markers)
        marker_min_c = min(c for r, c in markers)
        marker_max_c = max(c for r, c in markers)

        # Fill the intersection of marker bbox and gray rectangle
        fill_min_r = max(marker_min_r, min_r)
        fill_max_r = min(marker_max_r, max_r)
        fill_min_c = max(marker_min_c, min_c)
        fill_max_c = min(marker_max_c, max_c)

        for r in range(fill_min_r, fill_max_r + 1):
            for c in range(fill_min_c, fill_max_c + 1):
                # Fill gray cells or cells with the same color as the marker
                if output_grid[r][c] == 5 or output_grid[r][c] == color:
                    output_grid[r][c] = color

    # Remove markers that are outside the gray rectangle
    for color, marker_list in markers_by_color.items():
        for r, c in marker_list:
            # If marker is outside the gray rectangle, remove it
            if r < min_r or r > max_r or c < min_c or c > max_c:
                output_grid[r][c] = 0

    return Grid(output_grid)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("1c02dbbe", solve)
