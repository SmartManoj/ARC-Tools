import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Mirror and color-swap across a divider line

    1. Find the divider line (all 1s - either a horizontal row or vertical column)
    2. Identify which side has the pattern (non-zero, non-1 values)
    3. Find the two colors used in the pattern
    4. On the side WITH the pattern: swap the two colors
    5. On the OPPOSITE (empty) side: place the mirrored original pattern (no color swap)
    '''
    height = grid.height
    width = grid.width

    # Create output as a copy of input
    output_data = [row[:] for row in grid]

    # Find divider line (all 1s)
    divider_row = None
    divider_col = None

    for r in range(height):
        if all(grid[r][c] == 1 for c in range(width)):
            divider_row = r
            break

    if divider_row is None:
        for c in range(width):
            if all(grid[r][c] == 1 for r in range(height)):
                divider_col = c
                break

    # Find the two non-background colors (excluding 0 and 1)
    colors = set()
    for r in range(height):
        for c in range(width):
            if grid[r][c] not in [0, 1]:
                colors.add(grid[r][c])

    if len(colors) != 2:
        # If not exactly 2 colors, just return the grid as is
        return grid

    color1, color2 = sorted(colors)

    if divider_row is not None:
        # Horizontal divider - mirror vertically
        # Check which side has the pattern
        has_pattern_above = any(grid[r][c] in colors for r in range(divider_row) for c in range(width))

        if has_pattern_above:
            # Pattern is above - swap colors above, mirror to below
            for r in range(divider_row):
                for c in range(width):
                    if output_data[r][c] == color1:
                        output_data[r][c] = color2
                    elif output_data[r][c] == color2:
                        output_data[r][c] = color1

            # Mirror original pattern to below at same distance from divider
            for r in range(divider_row):
                offset = divider_row - r  # Distance from divider
                mirror_row = divider_row + offset
                if mirror_row < height:
                    for c in range(width):
                        output_data[mirror_row][c] = grid[r][c]
        else:
            # Pattern is below - swap colors below, mirror to above
            for r in range(divider_row + 1, height):
                for c in range(width):
                    if output_data[r][c] == color1:
                        output_data[r][c] = color2
                    elif output_data[r][c] == color2:
                        output_data[r][c] = color1

            # Mirror original pattern to above at same distance from divider
            for r in range(divider_row + 1, height):
                offset = r - divider_row  # Distance from divider
                mirror_row = divider_row - offset
                if mirror_row >= 0:
                    for c in range(width):
                        output_data[mirror_row][c] = grid[r][c]

    elif divider_col is not None:
        # Vertical divider - mirror horizontally
        # Check which side has the pattern
        has_pattern_right = any(grid[r][c] in colors for r in range(height) for c in range(divider_col + 1, width))

        if has_pattern_right:
            # Pattern is on right - swap colors on right, mirror to left
            for r in range(height):
                for c in range(divider_col + 1, width):
                    if output_data[r][c] == color1:
                        output_data[r][c] = color2
                    elif output_data[r][c] == color2:
                        output_data[r][c] = color1

            # Mirror original pattern to left at same distance from divider
            for c in range(divider_col + 1, width):
                offset = c - divider_col  # Distance from divider
                mirror_col = divider_col - offset
                if mirror_col >= 0:
                    for r in range(height):
                        output_data[r][mirror_col] = grid[r][c]
        else:
            # Pattern is on left - swap colors on left, mirror to right
            for r in range(height):
                for c in range(divider_col):
                    if output_data[r][c] == color1:
                        output_data[r][c] = color2
                    elif output_data[r][c] == color2:
                        output_data[r][c] = color1

            # Mirror original pattern to right at same distance from divider
            for c in range(divider_col):
                offset = divider_col - c  # Distance from divider
                mirror_col = divider_col + offset
                if mirror_col < width:
                    for r in range(height):
                        output_data[r][mirror_col] = grid[r][c]

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("2b01abd0", solve)
