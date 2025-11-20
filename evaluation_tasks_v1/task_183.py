import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transform the grid based on a "marker" pattern using 2s:
    - Rows with 2s divide the grid into regions
    - Fill above the first 2s row with 0
    - Fill below the last 2s row with the fill color
    - In marker rows: preserve 2s, fill non-2s with 0 (first marker) or fill_color (last marker)
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find first and last rows with 2s
    first_marker = -1
    last_marker = -1
    for r in range(h):
        if 2 in result[r]:
            if first_marker == -1:
                first_marker = r
            last_marker = r

    if first_marker == -1:
        return result

    # Find the fill color (non-0, non-2 color)
    colors = set()
    for r in range(h):
        for c in range(w):
            if result[r][c] != 0 and result[r][c] != 2:
                colors.add(result[r][c])

    fill_color = colors.pop() if colors else 0

    # Fill above first_marker with 0
    for r in range(first_marker):
        for c in range(w):
            result[r][c] = 0

    # For rows from first_marker to last_marker: preserve 2s
    for r in range(first_marker, last_marker + 1):
        if r == first_marker:
            # First marker row: fill non-2s with 0
            for c in range(w):
                if result[r][c] != 2:
                    result[r][c] = 0
        elif r == last_marker:
            # Last marker row: fill non-2s with fill_color or 0 based on pattern
            two_positions = [c for c in range(w) if result[r][c] == 2]
            is_consecutive = len(two_positions) > 1 and max(two_positions) - min(two_positions) == len(two_positions) - 1

            if is_consecutive:
                # Diagonal pattern: left of 2s fills with fill_color, right fills with 0
                min_col = min(two_positions)
                max_col = max(two_positions)
                for c in range(w):
                    if result[r][c] != 2:
                        if c < min_col:
                            result[r][c] = fill_color
                        elif c > max_col:
                            result[r][c] = 0
            else:
                # Non-consecutive pattern: all non-2s fill with fill_color
                for c in range(w):
                    if result[r][c] != 2:
                        result[r][c] = fill_color
        else:
            # Middle rows: check if 2s form a diagonal pattern (consecutive) or scattered pattern
            two_positions = [c for c in range(w) if result[r][c] == 2]
            if not two_positions:
                # No 2s in this row, fill with 0
                for c in range(w):
                    result[r][c] = 0
            elif len(two_positions) > 1 and max(two_positions) - min(two_positions) == len(two_positions) - 1:
                # Diagonal pattern: 2s are consecutive
                # Left of min_col gets special treatment, right of max_col gets 0
                min_col = min(two_positions)
                max_col = max(two_positions)
                for c in range(w):
                    if result[r][c] != 2:
                        if c < min_col:
                            # Left of 2s: fill with 0 if early, fill_color if late
                            if r <= first_marker + 1:
                                result[r][c] = 0
                            else:
                                result[r][c] = fill_color
                        elif c > max_col:
                            # Right of 2s: fill with 0
                            result[r][c] = 0
            else:
                # Scattered/alternating pattern: alternate fill_color and 0 based on segments
                for c in range(w):
                    if result[r][c] != 2:
                        # Count how many 2s are before this cell
                        num_twos_before = sum(1 for pos in two_positions if pos < c)
                        # Even segments (0, 2, 4...) get fill_color, odd (1, 3...) get 0
                        if num_twos_before % 2 == 0:
                            result[r][c] = fill_color
                        else:
                            result[r][c] = 0

    # Fill below last_marker with fill_color
    for r in range(last_marker + 1, h):
        for c in range(w):
            result[r][c] = fill_color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("782b5218", solve)
