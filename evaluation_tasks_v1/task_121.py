import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Extracts content between marker colors 1 and 8 on each row.

    Pattern:
    1. Find all rows that contain both color 1 and color 8
    2. For each such row, extract the values between the positions of 1 and 8 (exclusive)
    3. Stack these extracted segments to form the output grid
    '''
    output_rows = []

    for row_idx in range(grid.height):
        row = [grid[row_idx][col_idx] for col_idx in range(grid.width)]

        # Check if this row contains both markers
        if 1 in row and 8 in row:
            # Find positions of markers
            col_1 = row.index(1)
            col_8 = row.index(8)

            # Extract values between markers (exclusive)
            # Handle both cases: 1 before 8 or 8 before 1
            start = min(col_1, col_8) + 1
            end = max(col_1, col_8)
            extracted = row[start:end]

            output_rows.append(extracted)

    return Grid(output_rows)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("505fff84", solve)
