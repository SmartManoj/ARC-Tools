import os
import numpy as np
from arc_tools.grid import Grid, Color
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms a grid with two horizontal dividing lines by extending marked regions (color 4).

    Pattern:
    1. Find two horizontal dividing lines: one of 8s, one of 2s
    2. Find all columns containing 4 in the top section (above first divider)
    3. For each such column:
       - Replace original 4s with 3s in top section
       - Fill downward to first divider with 4s
       - Fill through middle section with 8s
       - Replace 2 in second divider with 8
       - Fill bottom section with 8s, transitioning to 2s (mirroring top pattern)
    '''
    # Convert to numpy array for easier manipulation
    data = np.array(list(grid))
    height, width = data.shape

    # Find the two dividing lines (can be horizontal or vertical)
    div1 = None  # Line of 8s
    div2 = None  # Line of 2s
    is_horizontal = True

    # Check for horizontal dividing lines first
    for row in range(height):
        if np.all(data[row] == 8):
            div1 = row
        if np.all(data[row] == 2):
            div2 = row

    # If not found, check for vertical dividing lines
    if div1 is None or div2 is None:
        is_horizontal = False
        for col in range(width):
            if np.all(data[:, col] == 8):
                div1 = col
            if np.all(data[:, col] == 2):
                div2 = col

    if div1 is None or div2 is None:
        logger.debug(f"Dividers not found: div1={div1}, div2={div2}")
        return grid

    if is_horizontal:
        logger.debug(f"Horizontal dividers: First (8s) at row {div1}, Second (2s) at row {div2}")
    else:
        logger.debug(f"Vertical dividers: First (8s) at col {div1}, Second (2s) at col {div2}")

    # Create output grid (copy of input)
    output = data.copy()

    if is_horizontal:
        # Horizontal dividers: process columns, fill rows
        # Find all columns that contain 4 in the top section (above div1)
        cols_with_4 = set()
        four_positions = {}  # col -> list of rows with 4

        for row in range(div1):
            for col in range(width):
                if data[row][col] == 4:
                    cols_with_4.add(col)
                    if col not in four_positions:
                        four_positions[col] = []
                    four_positions[col].append(row)

        logger.debug(f"Columns with 4 in top section: {sorted(cols_with_4)}")

        # Process each column with 4
        for col in cols_with_4:
            rows_with_4 = four_positions[col]
            min_row = min(rows_with_4)
            max_row = max(rows_with_4)

            # Step 1: Replace original 4s with 3s in top section
            for row in rows_with_4:
                output[row][col] = 3

            # Step 2: Fill downward from max_row+1 to div1-1 with 4s
            for row in range(max_row + 1, div1):
                output[row][col] = 4

            # Step 3: Fill from div1+1 to div2-1 with 8s (middle section)
            for row in range(div1 + 1, div2):
                output[row][col] = 8

            # Step 4: Replace 2 with 8 in the second divider
            output[div2][col] = 8

            # Step 5: Fill bottom section with 8s, then transition to 2s at the end
            # Count consecutive 2s in input going upward from div2-1
            consecutive_2s = 0
            for check_row in range(div2 - 1, div1, -1):
                if data[check_row][col] == 2:
                    consecutive_2s += 1
                else:
                    break

            # Number of rows with 2 at the end = consecutive_2s + 1
            num_2s_at_end = consecutive_2s + 1

            for row in range(div2 + 1, height):
                if row >= height - num_2s_at_end:
                    output[row][col] = 2
                else:
                    output[row][col] = 8

    else:
        # Vertical dividers: process rows, fill columns
        # Find all rows that contain 4 in the left section (before div1)
        rows_with_4 = set()
        four_positions = {}  # row -> list of cols with 4

        for col in range(div1):
            for row in range(height):
                if data[row][col] == 4:
                    rows_with_4.add(row)
                    if row not in four_positions:
                        four_positions[row] = []
                    four_positions[row].append(col)

        logger.debug(f"Rows with 4 in left section: {sorted(rows_with_4)}")

        # Process each row with 4
        for row in rows_with_4:
            cols_with_4_in_row = four_positions[row]
            min_col = min(cols_with_4_in_row)
            max_col = max(cols_with_4_in_row)

            # Step 1: Replace original 4s with 3s in left section
            for col in cols_with_4_in_row:
                output[row][col] = 3

            # Step 2: Fill rightward from max_col+1 to div1-1 with 4s
            for col in range(max_col + 1, div1):
                output[row][col] = 4

            # Step 3: Fill from div1+1 to div2-1 with 8s (middle section)
            for col in range(div1 + 1, div2):
                output[row][col] = 8

            # Step 4: Replace 2 with 8 in the second divider
            output[row][div2] = 8

            # Step 5: Fill right section with 8s, then transition to 2s at the end
            # Count consecutive 2s in input going leftward from div2-1
            consecutive_2s = 0
            for check_col in range(div2 - 1, div1, -1):
                if data[row][check_col] == 2:
                    consecutive_2s += 1
                else:
                    break

            # Number of columns with 2 at the end = consecutive_2s + 1
            num_2s_at_end = consecutive_2s + 1

            for col in range(div2 + 1, width):
                if col >= width - num_2s_at_end:
                    output[row][col] = 2
                else:
                    output[row][col] = 8

    return Grid(output.tolist())

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("05a7bcf2", solve)
