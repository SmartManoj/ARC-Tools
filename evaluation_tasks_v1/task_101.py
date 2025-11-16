import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: The grid contains colored rectangles (5x5 blocks) separated by black borders.
    Each rectangle has a colored border and a 3x3 inner pattern.
    When multiple rectangles share the same color, copy the non-empty inner pattern
    to all rectangles with that color.

    Algorithm:
    1. Identify all rectangles by their grid positions
    2. Extract color and inner 3x3 pattern for each rectangle
    3. Group rectangles by color
    4. For each color group, find the pattern with non-zero values and apply it to all
    5. Reconstruct the output grid
    '''
    output = Grid([[cell for cell in row] for row in grid])

    # Find all rectangle positions (they start at rows/cols: 1, 7, 13, 19, etc.)
    # and are 5x5 in size
    rectangles = []

    # Scan for rectangles - they're separated by rows/cols of 0s
    # Check where rectangles start (after a row/col of mostly 0s)
    row_starts = []
    col_starts = []

    # Find row starts - look for transitions from 0-rows to non-0-rows
    for r in range(len(grid)):
        if r == 0:
            continue
        # Check if previous row was mostly 0s and current row has colors
        prev_row_colors = [grid[r-1][c] for c in range(len(grid[0]))]
        curr_row_colors = [grid[r][c] for c in range(len(grid[0]))]
        if max(prev_row_colors) == 0 and max(curr_row_colors) > 0:
            row_starts.append(r)

    # Find col starts - look for transitions from 0-cols to non-0-cols
    for c in range(len(grid[0])):
        if c == 0:
            continue
        # Check if previous col was mostly 0s and current col has colors
        prev_col_colors = [grid[r][c-1] for r in range(len(grid))]
        curr_col_colors = [grid[r][c] for r in range(len(grid))]
        if max(prev_col_colors) == 0 and max(curr_col_colors) > 0:
            col_starts.append(c)

    # Extract rectangle info
    for r_start in row_starts:
        for c_start in col_starts:
            # Get the color of this rectangle (from the border)
            color = grid[r_start][c_start]

            # Extract inner 3x3 pattern (rows r_start+1 to r_start+3, cols c_start+1 to c_start+3)
            inner_pattern = []
            for r in range(r_start + 1, r_start + 4):
                row_pattern = []
                for c in range(c_start + 1, c_start + 4):
                    row_pattern.append(grid[r][c])
                inner_pattern.append(row_pattern)

            rectangles.append({
                'row': r_start,
                'col': c_start,
                'color': color,
                'pattern': inner_pattern
            })

    # Group rectangles by color
    color_groups = {}
    for rect in rectangles:
        color = rect['color']
        if color not in color_groups:
            color_groups[color] = []
        color_groups[color].append(rect)

    # For each color group, find the non-empty pattern and apply it
    for color, rects in color_groups.items():
        # Find the pattern that's not all 0s (or mostly 0s)
        source_pattern = None
        for rect in rects:
            pattern = rect['pattern']
            # Count non-zero and non-color values in the pattern
            has_content = False
            for row in pattern:
                for val in row:
                    if val != 0 and val != color:
                        has_content = True
                        break
                if has_content:
                    break

            # Also check if there are color values in non-trivial positions
            if not has_content:
                # Check for patterns with the same color arranged non-trivially
                flat = [val for row in pattern for val in row]
                if flat.count(color) > 0 and flat.count(color) < 9:
                    has_content = True

            if has_content:
                source_pattern = pattern
                break

        # If we found a source pattern, apply it to all rectangles of this color
        if source_pattern:
            for rect in rects:
                r_start = rect['row']
                c_start = rect['col']
                # Copy the pattern to this rectangle's inner 3x3
                for i, r in enumerate(range(r_start + 1, r_start + 4)):
                    for j, c in enumerate(range(c_start + 1, c_start + 4)):
                        output[r][c] = source_pattern[i][j]

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("42918530", solve)
