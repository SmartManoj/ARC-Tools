import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    The input is divided into cells by separator lines (a color that fills entire rows and columns).
    Each cell contains a single non-background color (or is empty/background).

    Algorithm:
    1. Identify the separator color (fills complete rows/columns)
    2. Extract the color from each cell
    3. For each unique non-background, non-separator color, count how many cells contain it
    4. Create output rows with each color repeated by its count, padded with 0s
    5. Sort rows by count (ascending)
    6. Output dimensions: height = number of colors, width = number of cell columns
    '''
    data = [row[:] for row in grid]
    h, w = len(data), len(data[0])

    # Find separator color (appears in full rows/columns)
    separator = None

    # Check for rows that are all the same non-zero color
    for color_candidate in range(1, 10):
        full_rows = [i for i in range(h) if all(data[i][j] == color_candidate for j in range(w))]
        full_cols = [j for j in range(w) if all(data[i][j] == color_candidate for i in range(h))]

        if full_rows and full_cols:
            separator = color_candidate
            break

    if separator is None:
        # No separator found, return empty result
        return Grid([[0]])

    # Find all positions of full rows and columns for the separator
    sep_rows = [i for i in range(h) if all(data[i][j] == separator for j in range(w))]
    sep_cols = [j for j in range(w) if all(data[i][j] == separator for i in range(h))]

    # Create cell boundaries
    row_boundaries = [-1] + sep_rows + [h]
    col_boundaries = [-1] + sep_cols + [w]

    # Extract cell ranges
    cell_row_ranges = []
    for i in range(len(row_boundaries) - 1):
        r_start = row_boundaries[i] + 1
        r_end = row_boundaries[i + 1]
        if r_start < r_end:
            cell_row_ranges.append((r_start, r_end))

    cell_col_ranges = []
    for i in range(len(col_boundaries) - 1):
        c_start = col_boundaries[i] + 1
        c_end = col_boundaries[i + 1]
        if c_start < c_end:
            cell_col_ranges.append((c_start, c_end))

    num_cell_cols = len(cell_col_ranges)

    # Extract the dominant color from each cell
    cell_colors = {}
    color_counts = {}  # Track how many cells each color appears in

    for ri, (r_start, r_end) in enumerate(cell_row_ranges):
        for ci, (c_start, c_end) in enumerate(cell_col_ranges):
            # Extract colors from this cell (excluding background 0 and separator)
            cell_colors_list = []
            for r in range(r_start, r_end):
                for c in range(c_start, c_end):
                    val = data[r][c]
                    if val != 0 and val != separator:
                        cell_colors_list.append(val)

            # Get the most common non-background, non-separator color
            if cell_colors_list:
                color = max(set(cell_colors_list), key=cell_colors_list.count)
            else:
                color = 0

            cell_colors[(ri, ci)] = color

            # Track color count
            if color != 0 and color != separator:
                color_counts[color] = color_counts.get(color, 0) + 1

    # Sort colors by their count (ascending), then by color value for tie-breaking
    sorted_colors = sorted(color_counts.items(), key=lambda x: (x[1], x[0]))

    # Output width is the maximum count of any color
    output_width = max(color_counts.values()) if color_counts else 1

    # Create output grid
    output_rows = []
    for color, count in sorted_colors:
        # Create row with color repeated 'count' times, padded with 0s
        row = [color] * count + [0] * (output_width - count)
        output_rows.append(row)

    # Convert to Grid
    if output_rows:
        result = Grid(output_rows)
    else:
        result = Grid([[0]])

    return result


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("81c0276b", solve)
