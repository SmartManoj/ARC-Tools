import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: For each yellow (4) rectangle in the input:
    1. Find the unique non-4 color(s) inside (marker colors)
    2. Count how many markers of that color exist
    3. Create a border around the rectangle using the marker color
    4. Border thickness = number of markers of that color
    '''
    # Create output as a 2D list (we'll convert to Grid at the end)
    output = [[grid[r][c] for c in range(grid.width)] for r in range(grid.height)]

    # Find all cells containing yellow (4) or non-zero, non-background colors
    # Scan for rectangular regions
    visited = [[False] * grid.width for _ in range(grid.height)]
    rectangles = []

    for r in range(grid.height):
        for c in range(grid.width):
            if visited[r][c] or grid[r][c] == 0:
                continue

            # Check if this cell is part of a yellow rectangle
            if grid[r][c] != 4:
                # If it's a marker, skip it for now
                continue

            # Found a yellow cell, find the bounding box by flood filling
            # Find all connected cells (yellow or markers within the rectangle)
            min_row, max_row = r, r
            min_col, max_col = c, c

            # Expand the bounding box to include all adjacent non-background cells
            # Go down and up to find row extent
            for rr in range(r, grid.height):
                if grid[rr][c] == 0:
                    break
                max_row = rr

            for rr in range(r, -1, -1):
                if grid[rr][c] == 0:
                    break
                min_row = rr

            # Go right and left to find column extent
            for cc in range(c, grid.width):
                if grid[r][cc] == 0:
                    break
                max_col = cc

            for cc in range(c, -1, -1):
                if grid[r][cc] == 0:
                    break
                min_col = cc


            # Mark all cells in this rectangle as visited
            for rr in range(min_row, max_row + 1):
                for cc in range(min_col, max_col + 1):
                    visited[rr][cc] = True

            rectangles.append((min_row, max_row, min_col, max_col))

    # Process each rectangle
    for min_row, max_row, min_col, max_col in rectangles:
        # Find the marker color and count within this rectangle
        marker_colors = {}
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                color = grid[r][c]
                if color != 4 and color != 0:  # Not yellow and not black
                    marker_colors[color] = marker_colors.get(color, 0) + 1

        # Should have at least one marker color
        if len(marker_colors) == 0:
            continue

        # Use the first marker color (should only be one)
        marker_color = list(marker_colors.keys())[0]
        count = marker_colors[marker_color]

        # Create border with thickness = count
        # Fill the entire border area (rectangular frame)
        border_min_row = max(0, min_row - count)
        border_max_row = min(grid.height - 1, max_row + count)
        border_min_col = max(0, min_col - count)
        border_max_col = min(grid.width - 1, max_col + count)

        for r in range(border_min_row, border_max_row + 1):
            for c in range(border_min_col, border_max_col + 1):
                # Draw if in border area (not in the inner rectangle)
                if r < min_row or r > max_row or c < min_col or c > max_col:
                    output[r][c] = marker_color

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("52fd389e", solve)
