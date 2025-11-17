import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transform the grid based on a horizontal line of 2s acting as a mirror.
    For 4s above the line:
    - If distance >= 3: move down 1 row (toward the line)
    - If distance == 2: create a diamond pattern pointing toward the line
    For 4s below the line:
    - Move further away by 1 row
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find the line of 2s (horizontal line)
    line_row = -1
    for r in range(h):
        if all(result[r][c] == 2 for c in range(w)):
            line_row = r
            break

    if line_row == -1:
        return result

    # Find all 4s in the input
    fours = []
    for r in range(h):
        for c in range(w):
            if result[r][c] == 4:
                fours.append((r, c))

    # Clear existing 4s
    for r, c in fours:
        result[r][c] = 0

    # Process each 4
    for r, c in fours:
        distance = abs(r - line_row)
        is_above = r < line_row

        if is_above:
            # 4 is above the line
            if distance >= 3:
                # Move down 1 row toward the line
                new_r = r + 1
                if 0 <= new_r < h and new_r != line_row:
                    result[new_r][c] = 4
            elif distance == 2:
                # Create diamond pattern pointing toward the line
                # Row away from line (r-1): distance 2 from center col
                # Row same (r): distance 1 from center col
                # Row toward line (r+1): distance 0 from center col

                # Row away from line - also extend diagonals further away
                away_r = r - 1
                away_cols = []
                if away_r >= 0:
                    if c - 2 >= 0:
                        result[away_r][c - 2] = 4
                        away_cols.append(c - 2)
                    if c + 2 < w:
                        result[away_r][c + 2] = 4
                        away_cols.append(c + 2)

                # Extend diagonals from away positions further away from the line
                for away_c in away_cols:
                    # Determine if this is the left or right away position
                    is_left = away_c < c

                    if is_left:
                        # Extend left-upward diagonal (further away)
                        diag_r = away_r - 1
                        diag_c = away_c - 1
                        while diag_r >= 0 and diag_c >= 0:
                            result[diag_r][diag_c] = 4
                            diag_r -= 1
                            diag_c -= 1
                    else:
                        # Extend right-upward diagonal (further away)
                        diag_r = away_r - 1
                        diag_c = away_c + 1
                        while diag_r >= 0 and diag_c < w:
                            result[diag_r][diag_c] = 4
                            diag_r -= 1
                            diag_c += 1

                # Same row
                if c - 1 >= 0:
                    result[r][c - 1] = 4
                if c + 1 < w:
                    result[r][c + 1] = 4

                # Row toward line
                toward_r = r + 1
                if toward_r < line_row and toward_r != line_row:
                    result[toward_r][c] = 4
        else:
            # 4 is below the line
            # Move further away by 1 row
            new_r = r + 1
            if new_r < h:
                result[new_r][c] = 4

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("73c3b0d8", solve)
