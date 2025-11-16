import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern analysis:
    1. Some rows contain sequences (2+ consecutive non-zero values)
    2. Other rows contain isolated marker pixels (single non-zero value)
    3. For each isolated marker pixel:
       - Find which sequence contains that color value
       - Find the index of that value in the sequence
       - Place the sequence in the pixel's row, positioned so the matching value aligns with the pixel's column
       - If the alignment would place part of the sequence before column 0, truncate the beginning
    '''
    height = len(grid)
    width = len(grid[0])

    # Create output grid as a copy of input
    output_data = [list(row) for row in grid]

    # Extract all sequences from all rows
    # A sequence is 2+ consecutive non-zero values
    sequences = []
    row_has_sequence = [False] * height

    for r in range(height):
        row = list(grid[r])
        current_seq = []

        for val in row:
            if val != 0:
                current_seq.append(val)
            else:
                if len(current_seq) >= 2:
                    sequences.append(current_seq)
                    row_has_sequence[r] = True
                current_seq = []

        if len(current_seq) >= 2:
            sequences.append(current_seq)
            row_has_sequence[r] = True

    # Find all isolated marker pixels (rows without sequences)
    for r in range(height):
        if not row_has_sequence[r]:
            for c in range(width):
                pixel_value = grid[r][c]
                if pixel_value != 0:
                    # Find which sequence contains this value
                    for seq in sequences:
                        if pixel_value in seq:
                            # Find index of value in sequence
                            idx = seq.index(pixel_value)
                            # Calculate starting column to align the value at column c
                            start_col = c - idx

                            # Place the sequence in row r
                            for i, val in enumerate(seq):
                                target_col = start_col + i
                                if 0 <= target_col < width:
                                    output_data[r][target_col] = val
                            break

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("5af49b42", solve)
