import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task
import numpy as np

def solve(grid: Grid):
    '''
    Pattern Analysis:
    - Grid is divided by colored lines (dividers) into rectangular cells
    - Some cells contain colored patterns
    - Transform: For each color, reflect patterns both vertically and horizontally
      to complete rectangular blocks

    The transformation mirrors each colored pattern across both axes to fill in
    missing cells and create symmetric blocks.
    '''

    # Convert to numpy for easier manipulation
    data = np.array([[grid[r][c] for c in range(grid.width)] for r in range(grid.height)])
    h, w = data.shape

    # Find the divider color (most frequent non-zero color that forms lines)
    divider_color = None
    color_counts = {}
    for r in range(h):
        for c in range(w):
            val = data[r, c]
            if val != 0:
                color_counts[val] = color_counts.get(val, 0) + 1

    if color_counts:
        divider_color = max(color_counts, key=color_counts.get)
    else:
        return grid

    # Find horizontal and vertical divider lines
    h_dividers = []
    v_dividers = []

    # Find horizontal dividers (rows that are entirely the divider color)
    for r in range(h):
        if all(data[r, c] == divider_color for c in range(w)):
            h_dividers.append(r)

    # Find vertical dividers (columns that are entirely the divider color)
    for c in range(w):
        if all(data[r, c] == divider_color for r in range(h)):
            v_dividers.append(c)

    # Create cell boundaries
    h_bounds = [0] + h_dividers + [h]
    v_bounds = [0] + v_dividers + [w]

    # Extract cells (regions between dividers)
    cells = {}  # (i, j) -> (r1, r2, c1, c2)
    for i in range(len(h_bounds) - 1):
        for j in range(len(v_bounds) - 1):
            r1, r2 = h_bounds[i], h_bounds[i + 1]
            c1, c2 = v_bounds[j], v_bounds[j + 1]

            # Skip if it's a divider cell
            if r2 - r1 <= 1 or c2 - c1 <= 1:
                continue

            # Adjust to exclude divider rows/cols
            if r1 in h_dividers:
                r1 += 1
            if c1 in v_dividers:
                c1 += 1

            cells[(i, j)] = (r1, r2, c1, c2)

    # Create output as copy of input
    output = data.copy()

    # Get all unique colors (excluding background and divider)
    colors_in_grid = set()
    for val in data.flatten():
        if val != 0 and val != divider_color:
            colors_in_grid.add(val)

    # Process each color separately
    for color in colors_in_grid:
        # Find all cells containing this color
        cells_with_color = {}  # (i, j) -> pattern
        for (i, j), (r1, r2, c1, c2) in cells.items():
            cell_data = data[r1:r2, c1:c2]
            if color in cell_data:
                cells_with_color[(i, j)] = cell_data.copy()

        if not cells_with_color:
            continue

        # Find bounding box of cells with this color
        min_i = min(i for i, j in cells_with_color.keys())
        max_i = max(i for i, j in cells_with_color.keys())
        min_j = min(j for i, j in cells_with_color.keys())
        max_j = max(j for i, j in cells_with_color.keys())

        # Fill in missing cells within the bounding box
        for target_i in range(min_i, max_i + 1):
            for target_j in range(min_j, max_j + 1):
                if (target_i, target_j) in cells_with_color:
                    continue  # Already has pattern

                if (target_i, target_j) not in cells:
                    continue  # Not a valid cell

                # Find source cell to reflect from
                # Try to find adjacent cell with pattern
                source_i, source_j = None, None
                source_pattern = None

                # Look for horizontal neighbor
                if (target_i, min_j) in cells_with_color:
                    source_i, source_j = target_i, min_j
                elif (target_i, max_j) in cells_with_color:
                    source_i, source_j = target_i, max_j
                # Look for vertical neighbor
                elif (min_i, target_j) in cells_with_color:
                    source_i, source_j = min_i, target_j
                elif (max_i, target_j) in cells_with_color:
                    source_i, source_j = max_i, target_j
                # Look for diagonal
                else:
                    # Find any cell with pattern
                    for (si, sj) in cells_with_color.keys():
                        source_i, source_j = si, sj
                        break

                if source_i is None:
                    continue

                source_pattern = cells_with_color[(source_i, source_j)]

                # Get target cell bounds
                tr1, tr2, tc1, tc2 = cells[(target_i, target_j)]
                sr1, sr2, sc1, sc2 = cells[(source_i, source_j)]

                # Check if sizes match
                if (tr2 - tr1) != (sr2 - sr1) or (tc2 - tc1) != (sc2 - sc1):
                    continue

                # Determine which reflection to apply
                h_flip = (target_j != source_j)
                v_flip = (target_i != source_i)

                # Apply flips to pattern
                reflected_pattern = source_pattern.copy()
                if h_flip:
                    reflected_pattern = np.fliplr(reflected_pattern)
                if v_flip:
                    reflected_pattern = np.flipud(reflected_pattern)

                # Copy to output (only overwrite background pixels)
                for ri in range(tr2 - tr1):
                    for ci in range(tc2 - tc1):
                        if reflected_pattern[ri, ci] == color:
                            output[tr1 + ri, tc1 + ci] = color

    return Grid(output.tolist())

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("2546ccf6", solve)
