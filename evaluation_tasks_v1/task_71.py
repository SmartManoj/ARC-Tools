import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern Analysis:
    1. Find a 3-color horizontal pattern in the first row (left_color, middle_color, right_color)
    2. Find isolated pixels of each color elsewhere in the grid
    3. Transformation:
       - The pattern is replicated downward row by row
       - At the row containing an isolated pixel of a color, that color extends horizontally
       - After the row of an isolated pixel, that color stops appearing in the replicated pattern
       - The middle color always extends vertically through the entire grid
    '''
    height = grid.height
    width = grid.width

    # Create output grid initialized to 0
    output = [[0 for c in range(width)] for r in range(height)]

    # Find the 3-color pattern in the first row
    pattern_start = None
    left_color = None
    middle_color = None
    right_color = None

    for c in range(width - 2):
        if grid[0][c] != 0 and grid[0][c+1] != 0 and grid[0][c+2] != 0:
            pattern_start = c
            left_color = grid[0][c]
            middle_color = grid[0][c+1]
            right_color = grid[0][c+2]
            break

    if pattern_start is None:
        return grid

    left_col = pattern_start
    middle_col = pattern_start + 1
    right_col = pattern_start + 2

    # Find isolated pixels of each color (excluding the pattern in row 0)
    left_isolated = None
    middle_isolated = None
    right_isolated = None

    for r in range(1, height):
        for c in range(width):
            if grid[r][c] != 0:
                if grid[r][c] == left_color:
                    left_isolated = (r, c)
                elif grid[r][c] == middle_color:
                    middle_isolated = (r, c)
                elif grid[r][c] == right_color:
                    right_isolated = (r, c)

    # Determine the maximum row for each color
    left_max_row = left_isolated[0] if left_isolated else height - 1
    middle_max_row = middle_isolated[0] if middle_isolated else height - 1
    right_max_row = right_isolated[0] if right_isolated else height - 1

    # Find the overall max row to process
    max_row = max(left_max_row, middle_max_row, right_max_row)

    # Process each row
    for r in range(max_row + 1):
        # Left color: appears from row 0 to left_max_row
        if r <= left_max_row:
            output[r][left_col] = left_color
            # If this is the row with the isolated left pixel, extend horizontally
            if left_isolated and r == left_isolated[0]:
                start_c = min(left_col, left_isolated[1])
                end_c = max(left_col, left_isolated[1])
                for c in range(start_c, end_c + 1):
                    output[r][c] = left_color

        # Middle color: appears from row 0 to middle_max_row
        if r <= middle_max_row:
            output[r][middle_col] = middle_color
            # If this is the row with the isolated middle pixel, extend horizontally
            if middle_isolated and r == middle_isolated[0]:
                start_c = min(middle_col, middle_isolated[1])
                end_c = max(middle_col, middle_isolated[1])
                for c in range(start_c, end_c + 1):
                    output[r][c] = middle_color

        # Right color: appears from row 0 to right_max_row
        if r <= right_max_row:
            output[r][right_col] = right_color
            # If this is the row with the isolated right pixel, extend horizontally
            if right_isolated and r == right_isolated[0]:
                start_c = min(right_col, right_isolated[1])
                end_c = max(right_col, right_isolated[1])
                for c in range(start_c, end_c + 1):
                    output[r][c] = right_color

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("29700607", solve)
