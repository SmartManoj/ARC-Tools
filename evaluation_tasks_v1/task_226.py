import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Fill a rectangle with checkerboard pattern using colors from external markers.
    Find a rectangle formed by a border color (e.g., 5), find marker colors outside,
    and fill the rectangle interior with a checkerboard pattern of those colors.
    '''
    import numpy as np

    result = grid.copy()

    # Find all non-zero colors
    colors = set(grid.data[grid.data != 0].flatten())
    if len(colors) < 2:
        return grid

    # Find the most common non-zero color (likely the rectangle border)
    color_counts = {}
    for color in colors:
        color_counts[color] = np.sum(grid.data == color)

    border_color = max(color_counts, key=color_counts.get)
    marker_colors = [c for c in colors if c != border_color]

    # Find the rectangle bounds
    border_points = np.where(grid.data == border_color)
    if len(border_points[0]) == 0:
        return grid

    min_row, max_row = np.min(border_points[0]), np.max(border_points[0])
    min_col, max_col = np.min(border_points[1]), np.max(border_points[1])

    # Fill the interior with checkerboard pattern
    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            if len(marker_colors) >= 2:
                # Checkerboard pattern
                if ((r - min_row - 1) // 2 + (c - min_col - 1) // 2) % 2 == 0:
                    result.data[r, c] = marker_colors[0]
                else:
                    result.data[r, c] = marker_colors[1]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("94414823", solve)
