import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Mirror pattern across vertical line:
    - Find vertical line of color 2
    - Find 4-shaped pattern on one side
    - Find marker pixel (unique color)
    - Mirror the 4-pattern to the other side using marker color
    '''
    output = [[grid[i][j] for j in range(grid.width)] for i in range(grid.height)]

    # Find all vertical lines of color 2
    for col in range(grid.width):
        # Check if this column has 2s forming a vertical line
        twos_in_col = [(r, col) for r in range(grid.height) if grid[r][col] == 2]
        if len(twos_in_col) < 2:
            continue

        # Find the range of the vertical line
        min_row = min(r for r, c in twos_in_col)
        max_row = max(r for r, c in twos_in_col)

        # Check if it's a continuous vertical line
        if all(grid[r][col] == 2 for r in range(min_row, max_row + 1)):
            # Find the marker (unique color, not 0, 2, or 4)
            marker = None
            marker_pos = None
            for r in range(min_row, max_row + 1):
                for c in range(grid.width):
                    if grid[r][c] not in [0, 2, 4] and grid[r][c] != marker:
                        if marker is None:
                            marker = grid[r][c]
                            marker_pos = (r, c)

            if marker is None:
                continue

            # Determine which side has the 4s
            left_has_4 = any(grid[r][c] == 4 for r in range(min_row, max_row + 1) for c in range(col))
            right_has_4 = any(grid[r][c] == 4 for r in range(min_row, max_row + 1) for c in range(col + 1, grid.width))

            # Mirror the 4-pattern
            for r in range(min_row, max_row + 1):
                if left_has_4:
                    # Mirror left pattern to right
                    for offset in range(1, grid.width - col):
                        left_col = col - offset
                        right_col = col + offset
                        if 0 <= left_col < grid.width and 0 <= right_col < grid.width:
                            if grid[r][left_col] == 4:
                                output[r][right_col] = marker
                else:
                    # Mirror right pattern to left
                    for offset in range(1, col + 1):
                        right_col = col + offset
                        left_col = col - offset
                        if 0 <= right_col < grid.width and 0 <= left_col >= 0:
                            if grid[r][right_col] == 4:
                                output[r][left_col] = marker

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("88207623", solve)
