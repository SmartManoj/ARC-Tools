import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Take non-zero values from row 1 and replicate them horizontally based on:
    - Each value gets a first gap: 3*(n-1) + n*i (where n=number of values, i=position index)
    - Gaps increment by n^2 for subsequent repetitions
    - Continue replicating as long as position stays within grid width
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find all non-zero values in row 1
    if h < 2:
        return result

    row1 = result[1]
    non_zero_items = []
    for col in range(w):
        if row1[col] != 0:
            non_zero_items.append((col, row1[col]))

    if not non_zero_items:
        return result

    n = len(non_zero_items)

    # Calculate first_gap and increment based on number of values
    first_gap_base = 3 * (n - 1)
    increment = n * n

    # Clear row 1 and replicate values
    for col in range(w):
        if col not in [pos for pos, _ in non_zero_items]:
            row1[col] = 0

    # For each non-zero value, replicate it
    for idx, (pos, value) in enumerate(non_zero_items):
        # Calculate first gap for this value's position index
        first_gap = first_gap_base + n * idx

        # Place the original
        current_pos = pos
        gap_index = 0

        while current_pos < w:
            result[1][current_pos] = value

            # Calculate next gap
            gap = first_gap + gap_index * increment
            current_pos += gap
            gap_index += 1

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("72207abc", solve)
