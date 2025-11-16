import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Find 3x3 hollow square patterns and replicate them across rows
    to match the row that has the most instances.

    The 3x3 pattern is:
    1 1 1
    1 0 1
    1 1 1

    Steps:
    1. Detect all 3x3 hollow square patterns in the grid
    2. Group them by row position
    3. Find the row with the most patterns
    4. For other rows, replicate patterns to match that row's column positions
    5. Use color 8 (cyan) for the replicated copies
    '''

    # Create output grid as copy of input
    output = Grid([[cell for cell in row] for row in grid])

    # Define the 3x3 hollow square pattern
    pattern = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]

    # Find all pattern instances - store (row, col) of top-left corner
    pattern_positions = []
    for r in range(len(grid) - 2):
        for c in range(len(grid[0]) - 2):
            # Check if pattern matches at this position
            matches = True
            for pr in range(3):
                for pc in range(3):
                    if grid[r + pr][c + pc] != pattern[pr][pc]:
                        matches = False
                        break
                if not matches:
                    break
            if matches:
                pattern_positions.append((r, c))

    # Group patterns by row (using the row of the pattern center)
    row_to_cols = {}
    for r, c in pattern_positions:
        center_row = r + 1  # Middle row of the 3x3 pattern
        if center_row not in row_to_cols:
            row_to_cols[center_row] = []
        row_to_cols[center_row].append(c)

    # Find the row with the most patterns
    if not row_to_cols:
        return output

    max_row = max(row_to_cols.keys(), key=lambda r: len(row_to_cols[r]))
    reference_cols = sorted(row_to_cols[max_row])

    # For each other row, replicate patterns to match reference columns
    for row in row_to_cols.keys():
        if row == max_row:
            continue

        current_cols = sorted(row_to_cols[row])

        # Find which columns need to be added
        missing_cols = [c for c in reference_cols if c not in current_cols]

        # For each missing column, copy the pattern from an existing position
        if current_cols:
            source_col = current_cols[0]
            for target_col in missing_cols:
                # Copy the 3x3 pattern using color 8 (cyan)
                for pr in range(3):
                    for pc in range(3):
                        source_val = grid[row - 1 + pr][source_col + pc]
                        if source_val == 1:
                            output[row - 1 + pr][target_col + pc] = 8
                        else:
                            output[row - 1 + pr][target_col + pc] = source_val

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("5b526a93", solve)
