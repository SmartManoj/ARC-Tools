import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Find rectangular regions filled with a uniform value and replace them with color 4.

    Pattern:
    - Scan for rectangular regions (at least 5x5) that contain only one value
    - Replace those uniform rectangular regions with color 4
    - All other cells remain unchanged
    '''
    output_data = [[grid[r][c] for c in range(grid.width)] for r in range(grid.height)]
    height = grid.height
    width = grid.width

    # Track which cells have been processed to avoid overlapping regions
    processed = [[False] * width for _ in range(height)]

    # Find all rectangular regions of uniform values
    # Try to find the largest rectangle at each position by trying different widths
    for start_row in range(height):
        for start_col in range(width):
            if processed[start_row][start_col]:
                continue

            value = grid[start_row][start_col]

            # Find the maximum possible width in the first row
            max_possible_width = start_col
            while max_possible_width < width and grid[start_row][max_possible_width] == value and not processed[start_row][max_possible_width]:
                max_possible_width += 1
            max_possible_width -= start_col

            # Try different widths and find the one that gives the largest area
            best_rect = None
            best_area = 0

            for try_width in range(1, max_possible_width + 1):
                # Find max height with this width
                try_max_row = start_row
                valid = True
                while try_max_row < height and valid:
                    for col in range(start_col, start_col + try_width):
                        if col >= width or grid[try_max_row][col] != value or processed[try_max_row][col]:
                            valid = False
                            break
                    if valid:
                        try_max_row += 1

                try_height = try_max_row - start_row
                try_area = try_height * try_width

                # Check if this meets our criteria and is better than previous best
                if try_area >= 20 and try_height >= 4 and try_width >= 4 and try_area > best_area:
                    best_rect = (start_row, start_col, try_height, try_width)
                    best_area = try_area

            # If we found a valid rectangle, mark it
            if best_rect:
                rect_row, rect_col, rect_height, rect_width = best_rect
                # Replace this region with 4
                for r in range(rect_row, rect_row + rect_height):
                    for c in range(rect_col, rect_col + rect_width):
                        output_data[r][c] = 4
                        processed[r][c] = True

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("25094a63", solve)
