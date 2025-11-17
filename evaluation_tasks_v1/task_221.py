import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find a pattern in one cell of a grid and tile it to all cells.
    The grid is divided by lines (all same color), and one cell contains a pattern
    that should be replicated to all other cells.
    '''
    # Find the grid line color (appears frequently and creates lines)
    height, width = grid.shape

    # Find vertical and horizontal lines
    vertical_lines = []
    horizontal_lines = []

    # Check for vertical lines (columns that are all same color)
    for col in range(width):
        colors = set(grid.data[row, col] for row in range(height))
        if len(colors) == 1 and grid.data[0, col] != 0:
            vertical_lines.append(col)

    # Check for horizontal lines (rows that are all same color)
    for row in range(height):
        colors = set(grid.data[row, col] for col in range(width))
        if len(colors) == 1 and grid.data[row, 0] != 0:
            horizontal_lines.append(row)

    if not vertical_lines or not horizontal_lines:
        return grid

    # Get grid line color
    grid_color = grid.data[horizontal_lines[0], 0]

    # Determine cell boundaries
    cell_width = vertical_lines[1] - vertical_lines[0] if len(vertical_lines) > 1 else width
    cell_height = horizontal_lines[1] - horizontal_lines[0] if len(horizontal_lines) > 1 else height

    # Find the cell with a pattern (non-zero, non-grid-color values)
    pattern = None
    for h_idx in range(len(horizontal_lines) - 1):
        for v_idx in range(len(vertical_lines) - 1):
            row_start = horizontal_lines[h_idx] + 1
            row_end = horizontal_lines[h_idx + 1]
            col_start = vertical_lines[v_idx] + 1
            col_end = vertical_lines[v_idx + 1]

            # Check if this cell has a pattern
            has_pattern = False
            for r in range(row_start, row_end):
                for c in range(col_start, col_end):
                    if grid.data[r, c] != 0 and grid.data[r, c] != grid_color:
                        has_pattern = True
                        break
                if has_pattern:
                    break

            if has_pattern:
                # Extract the pattern
                pattern = []
                for r in range(row_start, row_end):
                    row_data = []
                    for c in range(col_start, col_end):
                        row_data.append(grid.data[r, c])
                    pattern.append(row_data)
                break
        if pattern:
            break

    if not pattern:
        return grid

    # Apply pattern to all cells
    result = grid.copy()
    for h_idx in range(len(horizontal_lines) - 1):
        for v_idx in range(len(vertical_lines) - 1):
            row_start = horizontal_lines[h_idx] + 1
            row_end = horizontal_lines[h_idx + 1]
            col_start = vertical_lines[v_idx] + 1
            col_end = vertical_lines[v_idx + 1]

            # Copy pattern to this cell
            for i, r in enumerate(range(row_start, row_end)):
                for j, c in enumerate(range(col_start, col_end)):
                    if i < len(pattern) and j < len(pattern[i]):
                        result.data[r, c] = pattern[i][j]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("92e50de0", solve)
