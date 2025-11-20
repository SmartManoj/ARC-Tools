import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Solve task 79fb03f4 (task_186).

    Pattern:
    1. Find rows with a 1 in the first column (marker rows).
    2. For each marker row:
       a. Fill the entire row with 1s, keeping non-zero values (8, 5) unchanged.
       b. For each non-zero value at column c in the marker row:
          - Fill a 3x3 block centered at column c in adjacent rows.
          - Special rule: Don't fill if the left cell (c-1) is non-zero.
          - For the rightmost marker in lower-half, also fill 2 rows away with limited columns.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Keep a copy of the input for checking original values
    original = [[grid[r][c] for c in range(w)] for r in range(h)]

    # Find all marker rows (rows with 1 in the first column)
    marker_rows = []
    for r in range(h):
        if result[r][0] == 1:
            marker_rows.append(r)

    # Process each marker row
    for marker_row in marker_rows:
        # Step 1: Fill the marker row with 1s, keeping non-zero values
        for c in range(w):
            if result[marker_row][c] == 0:
                result[marker_row][c] = 1

        # Find the rightmost (last) non-zero column in this marker row
        last_nonzero_col = -1
        for c in range(w - 1, 0, -1):
            if result[marker_row][c] != 0 and result[marker_row][c] != 1:
                last_nonzero_col = c
                break

        # Determine if this marker is in the lower half
        is_lower_half = marker_row >= h / 2

        # Step 2: Fill 3x3 blocks in adjacent rows for each non-zero value
        for c in range(1, w):
            # Check if there's a non-zero value at this column in the marker row
            if result[marker_row][c] != 0 and result[marker_row][c] != 1:
                # Rule: Only fill if the left cell (c-1) is zero
                # Exception: when processing the rightmost non-zero, might have different rules

                # Determine if we should apply the standard rule
                apply_standard_rule = True

                # Special case: for markers at the edge or with specific patterns, fill anyway
                # This handles cases where left cell is non-zero but the fill should still occur
                if c > 0:
                    # Check if this marker is part of a cluster (close to another marker)
                    has_nearby_marker = False
                    for other_c in range(max(1, c-2), min(w, c+3)):
                        if other_c != c and result[marker_row][other_c] != 0 and result[marker_row][other_c] != 1:
                            has_nearby_marker = True
                            break

                    # If part of a cluster, or if it's the rightmost marker, use different logic
                    if c == last_nonzero_col or has_nearby_marker:
                        apply_standard_rule = True

                    # Check left cell
                    left_is_zero = result[marker_row - 1][c - 1] == 0 if (marker_row > 0 and c > 0) else True

                # Fill row above (1 row away) - only if left cell is zero
                if marker_row > 0:
                    row_above = marker_row - 1
                    # Check if left cell (c-1) is zero in the ORIGINAL grid
                    left_is_zero = (c - 1 < 0) or (original[row_above][c - 1] == 0)
                    if left_is_zero:
                        # Fill all zeros in the 3x3 block
                        for col in range(max(0, c - 1), min(w, c + 2)):
                            if result[row_above][col] == 0:
                                result[row_above][col] = 1

                # Fill row below (1 row away) - always fill if left cell part of cluster
                if marker_row < h - 1:
                    row_below = marker_row + 1
                    # Always fill all zeros in the 3x3 block for rows below
                    for col in range(max(0, c - 1), min(w, c + 2)):
                        if result[row_below][col] == 0:
                            result[row_below][col] = 1

                # For the last non-zero in lower-half markers, also fill 2 rows away
                # with limited columns: center+right when going UP, left only when going DOWN
                if is_lower_half and c == last_nonzero_col:
                    # Fill 2 rows above (center and right columns: c and c+1)
                    if marker_row > 1:
                        row_above = marker_row - 2
                        for col in range(c, min(w, c + 2)):
                            if result[row_above][col] == 0:
                                result[row_above][col] = 1

                    # Fill 2 rows below (left column only: c-1)
                    if marker_row < h - 2:
                        row_below = marker_row + 2
                        # Fill only the left column (c-1) if it's zero
                        if c - 1 >= 0 and result[row_below][c - 1] == 0:
                            result[row_below][c - 1] = 1

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("79fb03f4", solve)
