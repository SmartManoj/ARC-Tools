import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms rectangular blocks filled with 1s by creating concentric layers:
    - Edge layer (distance 0 from edge): stays 1
    - Layer 1 (distance 1 from edge): becomes 2
    - Layer 2 (distance 2 from edge): becomes 3
    - Layer 3+ (distance 3+ from edge): becomes 2

    The transformation applies to each rectangular region of 1s independently.
    '''
    # Create output grid as a copy of input using Grid's copy method
    output = grid.copy()

    # Detect all objects (regions of non-zero values)
    objects = detect_objects(grid, ignore_colors=[0])

    # Process each object (rectangular block of 1s)
    for obj in objects:
        # Get all points in this object
        all_points = obj.all_points

        # Find bounding box from the points
        min_x = min(p.y for p in all_points)  # Note: GridPoint.y is the column (x-coordinate)
        max_x = max(p.y for p in all_points)
        min_y = min(p.x for p in all_points)  # Note: GridPoint.x is the row (y-coordinate)
        max_y = max(p.x for p in all_points)

        # For each point in the object
        for p in all_points:
            row = p.x  # row
            col = p.y  # column

            # Calculate minimum distance from any edge of the bounding box
            dist_from_top = row - min_y
            dist_from_bottom = max_y - row
            dist_from_left = col - min_x
            dist_from_right = max_x - col

            min_dist = min(dist_from_top, dist_from_bottom, dist_from_left, dist_from_right)

            # Assign color based on distance using Grid's set method
            if min_dist == 0:
                # Edge - keep as 1
                output.set(row, col, 1)
            elif min_dist == 1:
                # First inner layer - color 2
                output.set(row, col, 2)
            elif min_dist == 2:
                # Second inner layer - color 3
                output.set(row, col, 3)
            else:
                # Third+ inner layer - color 2
                output.set(row, col, 2)

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("516b51b7", solve)
