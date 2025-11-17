import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Move each green (3) pixel to be immediately adjacent to the rightmost
    azure (8) pixel that comes before it in the same row.

    If there's no azure pixel before a green pixel, move the green to the beginning of the row.
    Multiple greens with the same rightmost azure are placed consecutively.
    '''
    result = grid.copy()
    width, height = grid.shape

    for row in range(height):
        # Find all azure (8) and green (3) positions in this row
        azure_positions = []
        green_positions = []

        for col in range(width):
            val = grid[row][col]
            if val == 8:
                azure_positions.append(col)
            elif val == 3:
                green_positions.append(col)

        if not green_positions:
            continue

        # First, clear all green positions
        for green_col in green_positions:
            result[row][green_col] = 0

        # Group greens by their rightmost azure
        green_groups = {}
        for green_col in green_positions:
            # Find the rightmost azure before this green
            rightmost_azure = -1
            for azure_col in azure_positions:
                if azure_col < green_col:
                    rightmost_azure = azure_col

            if rightmost_azure not in green_groups:
                green_groups[rightmost_azure] = []
            green_groups[rightmost_azure].append(green_col)

        # Place greens at their new positions
        for rightmost_azure, greens in green_groups.items():
            if rightmost_azure == -1:
                # No azure before, place at beginning
                start_pos = 0
            else:
                # Place right after the rightmost azure
                start_pos = rightmost_azure + 1

            # Place all greens in this group consecutively
            for i, green_col in enumerate(greens):
                result[row][start_pos + i] = 3

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("9c56f360", solve)
