import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find groups of 8s separated by rows of all zeros.
    For each group, shift it right by an amount equal to its bounding box width.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Identify row ranges that contain 8s
    rows_with_8s = set()
    for r in range(h):
        for c in range(w):
            if result[r][c] == 8:
                rows_with_8s.add(r)

    # Group consecutive rows into separate groups
    groups = []
    current_group = []
    prev_row = None
    for r in sorted(rows_with_8s):
        if prev_row is not None and r > prev_row + 1:
            # Gap detected, start new group
            if current_group:
                groups.append(current_group)
            current_group = [r]
        else:
            current_group.append(r)
        prev_row = r
    if current_group:
        groups.append(current_group)

    # For each group, find all 8s in those rows and shift them
    for row_group in groups:
        # Find all 8s in this group of rows
        cells_in_group = []
        for r in row_group:
            for c in range(w):
                if result[r][c] == 8:
                    cells_in_group.append((r, c))

        if not cells_in_group:
            continue

        # Find bounding box
        min_col = min(c for r, c in cells_in_group)
        max_col = max(c for r, c in cells_in_group)
        width = max_col - min_col + 1

        # Shift amount equals width
        shift = width

        # Clear old positions
        for r, c in cells_in_group:
            result[r][c] = 0

        # Place at new positions (shift right by shift amount)
        for r, c in cells_in_group:
            new_c = c + shift
            if new_c < w:  # Only place if within grid bounds
                result[r][new_c] = 8

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("64a7c07e", solve)
