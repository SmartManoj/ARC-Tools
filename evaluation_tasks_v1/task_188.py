import os
from collections import Counter
from arc_tools.grid import Grid
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task


def solve(grid: Grid):
    '''
    The grid is divided by "divider" rows and columns (all non-zero values).
    These dividers create rectangular regions. Each region is filled by finding
    the non-zero, non-five color values in the bounding divider rows and columns,
    then filling all 0s in that region with the most frequent color.
    Tie-breaking: prefer row_below > row_above > higher value.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find row dividers (rows with all non-zero values)
    row_divs = []
    for r in range(h):
        if all(result[r][c] != 0 for c in range(w)):
            row_divs.append(r)

    # Find column dividers (columns with all non-zero values)
    col_divs = []
    for c in range(w):
        if all(result[r][c] != 0 for r in range(h)):
            col_divs.append(c)

    # Create row ranges (regions between row dividers)
    row_ranges = []
    prev = -1
    for rd in row_divs:
        if prev + 1 <= rd - 1:
            row_ranges.append((prev + 1, rd - 1))
        prev = rd
    if prev + 1 < h:
        row_ranges.append((prev + 1, h - 1))

    # Create column ranges (regions between column dividers)
    col_ranges = []
    prev = -1
    for cd in col_divs:
        if prev + 1 <= cd - 1:
            col_ranges.append((prev + 1, cd - 1))
        prev = cd
    if prev + 1 < w:
        col_ranges.append((prev + 1, w - 1))

    # For each rectangular region, determine and apply fill color
    for r_start, r_end in row_ranges:
        for c_start, c_end in col_ranges:
            # Find bounding dividers for this region
            row_above = max([rd for rd in row_divs if rd < r_start], default=None)
            row_below = min([rd for rd in row_divs if rd > r_end], default=None)
            col_left = max([cd for cd in col_divs if cd < c_start], default=None)
            col_right = min([cd for cd in col_divs if cd > c_end], default=None)

            # Collect values from bounding dividers with source tracking
            value_sources = {}  # value -> list of (source_type, index)

            # From row divider above
            if row_above is not None:
                for c in range(c_start, c_end + 1):
                    val = result[row_above][c]
                    if val not in [0, 5]:
                        if val not in value_sources:
                            value_sources[val] = []
                        value_sources[val].append(('row_above', row_above))

            # From row divider below
            if row_below is not None:
                for c in range(c_start, c_end + 1):
                    val = result[row_below][c]
                    if val not in [0, 5]:
                        if val not in value_sources:
                            value_sources[val] = []
                        value_sources[val].append(('row_below', row_below))

            # From column divider left
            if col_left is not None:
                for r in range(r_start, r_end + 1):
                    val = result[r][col_left]
                    if val not in [0, 5]:
                        if val not in value_sources:
                            value_sources[val] = []
                        value_sources[val].append(('col_left', col_left))

            # From column divider right
            if col_right is not None:
                for r in range(r_start, r_end + 1):
                    val = result[r][col_right]
                    if val not in [0, 5]:
                        if val not in value_sources:
                            value_sources[val] = []
                        value_sources[val].append(('col_right', col_right))

            # Count occurrences per value
            value_counts = {}
            for val, sources in value_sources.items():
                value_counts[val] = len(sources)

            # Determine fill color
            if value_counts:
                max_count = max(value_counts.values())
                candidates = [v for v, c in value_counts.items() if c == max_count]

                if len(candidates) == 1:
                    fill_color = candidates[0]
                else:
                    # Tie-breaking: prefer row_below, then row_above, then higher value
                    fill_color = None

                    # Try to find value from row_below
                    for v in candidates:
                        if any(src[0] == 'row_below' for src in value_sources[v]):
                            fill_color = v
                            break

                    # If not found, try row_above
                    if fill_color is None:
                        for v in candidates:
                            if any(src[0] == 'row_above' for src in value_sources[v]):
                                fill_color = v
                                break

                    # If still not found, use highest value
                    if fill_color is None:
                        fill_color = max(candidates)
            else:
                fill_color = 0

            # Fill all 0s in this region with the determined color
            for r in range(r_start, r_end + 1):
                for c in range(c_start, c_end + 1):
                    if result[r][c] == 0:
                        result[r][c] = fill_color

    return result


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("7c8af763", solve)
