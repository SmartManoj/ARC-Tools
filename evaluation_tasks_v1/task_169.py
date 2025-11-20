import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Task 169: Find the region of 5s and determine the fill color based on the
    closest non-5, non-0 color using Chebyshev distance.

    Algorithm:
    1. Find all cells containing 5s and compute their bounding box
    2. Find all non-0, non-5 colors in the grid
    3. For each color, compute minimum Chebyshev distance to the 5s bounding box
    4. Select the color with minimum distance (ties broken by smallest value)
    5. Fill all 5s with the selected color
    6. Clear everything else to 0
    '''
    result = Grid([[0] * grid.width for _ in range(grid.height)])
    h, w = grid.height, grid.width

    # Find all positions with 5s and compute bounding box
    fives_positions = []
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 5:
                fives_positions.append((r, c))

    if not fives_positions:
        return result

    # Compute bounding box of 5s
    min_r = min(pos[0] for pos in fives_positions)
    max_r = max(pos[0] for pos in fives_positions)
    min_c = min(pos[1] for pos in fives_positions)
    max_c = max(pos[1] for pos in fives_positions)

    # Find all non-0, non-5 colors and their positions
    color_positions = {}
    for r in range(h):
        for c in range(w):
            val = grid[r][c]
            if val != 0 and val != 5:
                if val not in color_positions:
                    color_positions[val] = []
                color_positions[val].append((r, c))

    # Compute Chebyshev distance from each color to the 5s bounding box
    def chebyshev_distance_to_box(positions, box_r_min, box_r_max, box_c_min, box_c_max):
        """Compute minimum Chebyshev distance from any position to the bounding box"""
        min_dist = float('inf')
        for r, c in positions:
            # Row distance
            if r < box_r_min:
                row_dist = box_r_min - r
            elif r > box_r_max:
                row_dist = r - box_r_max
            else:
                row_dist = 0

            # Column distance
            if c < box_c_min:
                col_dist = box_c_min - c
            elif c > box_c_max:
                col_dist = c - box_c_max
            else:
                col_dist = 0

            dist = max(row_dist, col_dist)
            min_dist = min(min_dist, dist)

        return min_dist

    # Find the color with minimum distance, with proper tie-breaking
    best_color = None
    best_distance = float('inf')
    best_min_component_dist = float('inf')

    def get_color_distances(positions, box_r_min, box_r_max, box_c_min, box_c_max):
        """
        Return the minimum Chebyshev distance and the minimum of row/col components for that distance
        """
        min_chebyshev = float('inf')
        min_component_for_best = float('inf')

        for r, c in positions:
            # Row distance
            if r < box_r_min:
                row_dist = box_r_min - r
            elif r > box_r_max:
                row_dist = r - box_r_max
            else:
                row_dist = 0

            # Column distance
            if c < box_c_min:
                col_dist = box_c_min - c
            elif c > box_c_max:
                col_dist = c - box_c_max
            else:
                col_dist = 0

            chebyshev_dist = max(row_dist, col_dist)
            min_component = min(row_dist, col_dist)

            if chebyshev_dist < min_chebyshev:
                min_chebyshev = chebyshev_dist
                min_component_for_best = min_component
            elif chebyshev_dist == min_chebyshev:
                min_component_for_best = min(min_component_for_best, min_component)

        return min_chebyshev, min_component_for_best

    for color, positions in color_positions.items():
        dist, min_component = get_color_distances(positions, min_r, max_r, min_c, max_c)

        # Update best color based on:
        # 1. Smallest Chebyshev distance
        # 2. If tied, smallest min(row_dist, col_dist)
        # 3. If tied, smallest color value
        if (dist < best_distance or
            (dist == best_distance and min_component < best_min_component_dist) or
            (dist == best_distance and min_component == best_min_component_dist and color < best_color)):
            best_color = color
            best_distance = dist
            best_min_component_dist = min_component

    # Fill the 5s with the best color
    if best_color is not None:
        for r, c in fives_positions:
            result[r][c] = best_color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("6df30ad6", solve)
