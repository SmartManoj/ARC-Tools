import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    Pattern: Rectangles made of 1s (with possible gaps in borders)
    - Fill interior with 8s
    - For each gap in a border, extend a line of 8s outward from the gap

    Steps:
    1. Find all rectangles (borders made of 1s)
    2. Fill interiors with 8s
    3. Detect gaps in borders and extend 8s outward
    '''
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Create output as a copy of input
    output = [[grid[r][c] for c in range(width)] for r in range(height)]

    # Find all rectangles by detecting their boundaries
    rectangles = find_rectangles(grid, height, width)

    # Process each rectangle
    for rect in rectangles:
        top, bottom, left, right = rect

        # Fill interior with 8s
        for r in range(top + 1, bottom):
            for c in range(left + 1, right):
                output[r][c] = 8

        # Check for gaps and extend 8s
        # Top border
        for c in range(left, right + 1):
            if grid[top][c] == 0:  # Gap in top border
                # Fill the gap and extend upward
                output[top][c] = 8
                for r in range(top - 1, -1, -1):
                    output[r][c] = 8

        # Bottom border
        for c in range(left, right + 1):
            if grid[bottom][c] == 0:  # Gap in bottom border
                # Fill the gap and extend downward
                output[bottom][c] = 8
                for r in range(bottom + 1, height):
                    output[r][c] = 8

        # Left border
        for r in range(top, bottom + 1):
            if grid[r][left] == 0:  # Gap in left border
                # Fill the gap and extend leftward
                output[r][left] = 8
                for c in range(left - 1, -1, -1):
                    output[r][c] = 8

        # Right border
        for r in range(top, bottom + 1):
            if grid[r][right] == 0:  # Gap in right border
                # Fill the gap and extend rightward
                output[r][right] = 8
                for c in range(right + 1, width):
                    output[r][c] = 8

    return Grid(output)


def find_rectangles(grid, height, width):
    '''
    Find all rectangles by detecting closed rectangular borders.
    Borders can have gaps but must be mostly made of 1s.
    '''
    rectangles = []
    used = [[False] * width for _ in range(height)]

    for top in range(height):
        for left in range(width):
            if grid[top][left] != 1 or used[top][left]:
                continue

            # Find extent by first getting continuous 1s
            right = left
            while right < width - 1 and grid[top][right + 1] == 1:
                right += 1

            # Then extend if there are more 1s after a small gap
            temp_right = right
            while temp_right < width - 1:
                # Look ahead up to 2 cells
                found_more = False
                for c in range(temp_right + 1, min(temp_right + 3, width)):
                    if grid[top][c] == 1:
                        # Check if there are enough 1s from current right to c
                        ones_in_range = sum(1 for cc in range(right, c + 1)
                                          if grid[top][cc] == 1)
                        if ones_in_range >= (c - right + 1) * 0.4:
                            right = c
                            temp_right = c
                            found_more = True
                            # Keep extending continuously from here
                            while right < width - 1 and grid[top][right + 1] == 1:
                                right += 1
                                temp_right = right
                            break
                if not found_more:
                    break

            # Require minimum width
            if right - left < 3:
                continue

            # Count 1s in top border to ensure it's mostly 1s
            top_ones = sum(1 for c in range(left, right + 1) if grid[top][c] == 1)
            if top_ones < (right - left + 1) * 0.6:
                continue

            # Find matching bottom border
            for bottom in range(top + 3, height):  # Minimum height of 4
                # Count 1s on bottom border
                bottom_ones = sum(1 for c in range(left, right + 1)
                                 if grid[bottom][c] == 1)

                # Need substantial overlap on bottom border
                if bottom_ones < (right - left + 1) * 0.7:
                    continue

                # Check vertical borders
                left_ones = sum(1 for r in range(top, bottom + 1)
                               if grid[r][left] == 1)
                right_ones = sum(1 for r in range(top, bottom + 1)
                                if grid[r][right] == 1)

                # Need mostly 1s on vertical borders
                if (left_ones < (bottom - top + 1) * 0.6 or
                    right_ones < (bottom - top + 1) * 0.6):
                    continue

                # Check interior is mostly empty
                interior_ones = sum(1 for r in range(top + 1, bottom)
                                   for c in range(left + 1, right)
                                   if grid[r][c] == 1)
                interior_total = (bottom - top - 1) * (right - left - 1)

                if interior_total > 0 and interior_ones / interior_total > 0.2:
                    continue

                # Found a valid rectangle
                rectangles.append((top, bottom, left, right))

                # Mark as used
                for r in range(top, bottom + 1):
                    for c in range(left, right + 1):
                        used[r][c] = True
                break

    return rectangles


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("551d5bf1", solve)
