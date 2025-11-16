import os
from arc_tools.grid import Grid, detect_objects, move_object
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Identifies distinct colored regions and shifts them alternately left and right.
    - 1st region (topmost): shift LEFT by 1
    - 2nd region: shift RIGHT by 1
    - 3rd region: shift LEFT by 1
    - 4th region: shift RIGHT by 1
    - And so on...
    '''
    # Start with background color filled grid
    background = grid.background_color
    result_data = [[background for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # Detect all colored objects (non-background regions)
    # Use single_color_only=True to separate regions by color
    objects = detect_objects(grid, single_color_only=True)

    # Sort objects by their topmost row position
    objects_sorted = sorted(objects, key=lambda obj: obj.region.y1)

    # Process each object and shift it
    for idx, obj in enumerate(objects_sorted):
        # Determine shift direction
        shift = -1 if idx % 2 == 0 else 1

        # Copy the object to the result with the shift applied
        for point in obj.points:
            new_col = point.x + shift
            # Make sure we stay within bounds
            if 0 <= new_col < len(grid[0]) and 0 <= point.y < len(grid):
                result_data[point.y][new_col] = grid[point.y][point.x]

    return Grid(result_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("4364c1c4", solve)
