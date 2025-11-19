import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Grid is divided by lines into sections. One section contains a template pattern.
    For each row of sections:
    - Find the 2x2 colored block to get the color
    - Apply the template pattern with that color to all sections in that row

    Steps:
    1. Find the divider color (appears as full rows/columns)
    2. Find the template pattern (non-trivial pattern in some section)
    3. For each row of sections, find the block color and apply template
    '''

    height = len(grid)
    width = len(grid[0])

    # Find divider color (most common in edges/lines)
    divider_color = None
    for row in range(height):
        if len(set(grid[row])) == 1:  # Full row of same color
            divider_color = grid[row][0]
            break

    # Find divider rows and columns
    divider_rows = []
    divider_cols = []

    for row in range(height):
        if all(grid[row][col] == divider_color for col in range(width)):
            divider_rows.append(row)

    for col in range(width):
        if all(grid[row][col] == divider_color for row in range(height)):
            divider_cols.append(col)

    # Create list of section ranges (between dividers)
    row_ranges = []
    prev = 0
    for div in divider_rows:
        if prev < div:
            row_ranges.append((prev, div))
        prev = div + 1
    if prev < height:
        row_ranges.append((prev, height))

    col_ranges = []
    prev = 0
    for div in divider_cols:
        if prev < div:
            col_ranges.append((prev, div))
        prev = div + 1
    if prev < width:
        col_ranges.append((prev, width))

    # Find the template pattern and the 2x2 blocks
    template_pattern = None
    template_size = None
    section_colors = {}  # (section_row, section_col) -> color

    for sr, (r_start, r_end) in enumerate(row_ranges):
        for sc, (c_start, c_end) in enumerate(col_ranges):
            # Extract section
            section = []
            for r in range(r_start, r_end):
                section.append([grid[r][c] for c in range(c_start, c_end)])

            # Count non-zero cells
            non_zero_count = sum(1 for row in section for cell in row if cell != 0)

            # Check for 2x2 block
            is_2x2_block = False
            block_color = None
            for r in range(len(section) - 1):
                for c in range(len(section[0]) - 1):
                    if (section[r][c] != 0 and
                        section[r][c] == section[r][c+1] ==
                        section[r+1][c] == section[r+1][c+1]):
                        is_2x2_block = True
                        block_color = section[r][c]
                        section_colors[(sr, sc)] = block_color
                        break
                if is_2x2_block:
                    break

            # Check if this is a template (more complex than just 2x2)
            if non_zero_count > 4 and not is_2x2_block:
                template_pattern = section
                template_size = (len(section), len(section[0]))
            elif non_zero_count == 4 and is_2x2_block:
                # Just a 2x2 block, record its color
                pass

    # Create output grid
    output = [[grid[r][c] for c in range(width)] for r in range(height)]

    # Apply template to all sections
    if template_pattern is not None:
        for sr, (r_start, r_end) in enumerate(row_ranges):
            # Find color for this row
            row_color = None
            for sc in range(len(col_ranges)):
                if (sr, sc) in section_colors:
                    row_color = section_colors[(sr, sc)]
                    break

            if row_color is not None:
                # Apply template to all sections in this row
                for sc, (c_start, c_end) in enumerate(col_ranges):
                    # Apply template
                    for dr in range(min(template_size[0], r_end - r_start)):
                        for dc in range(min(template_size[1], c_end - c_start)):
                            if template_pattern[dr][dc] != 0:
                                output[r_start + dr][c_start + dc] = row_color
                            else:
                                output[r_start + dr][c_start + dc] = 0

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("5a5a2103", solve)
