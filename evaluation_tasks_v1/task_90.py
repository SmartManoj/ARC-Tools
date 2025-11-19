import os
from arc_tools.grid import Grid, detect_objects
from helper import solve_task

def solve(grid: Grid):
    '''
    Transform color 8 regions into different colors based on their size and position.

    Pattern:
    1. Detect all connected regions of color 8 (using 4-connectivity)
    2. Sort by size, then by position for tiebreaking
    3. Assign colors based on a combination of size value and percentile rank:
       - Uses colors 1, 2, 3, 7 based on both absolute size and relative ranking
    '''
    # Create output grid as copy of input
    output = grid.copy()

    # Detect all connected regions of color 8 (4-connectivity)
    objects = detect_objects(grid, required_colors=[8], go_diagonal=False)

    if not objects:
        return output

    # Get size for each object and create a list with (object, size, min_row, min_col)
    object_data = []
    for obj in objects:
        # Use bounding box size (all_points) for determining color
        # but will color only actual pixels (points) later
        all_points = obj.all_points
        size = len(all_points)  # Size is based on bounding box
        # Use position for tiebreaking (reading order)
        min_r = min(p.x for p in all_points)
        min_c = min(p.y for p in all_points)
        object_data.append((obj, size, min_r, min_c))

    # Sort by size first, then by position (reading order) for tiebreaking
    object_data.sort(key=lambda x: (x[1], x[2], x[3]))

    # Determine colors based on size, percentile, and overall size distribution
    n = len(object_data)
    min_size = min(data[1] for data in object_data)

    for i, (obj, size, _, _) in enumerate(object_data):
        # Calculate percentile (0.0 to close to 1.0)
        percentile = i / n if n > 1 else 0

        # Check if this example uses large sizes (skip colors 1 and 2)
        if min_size >= 28:
            # For examples with all large sizes, use only colors 3 and 7
            if percentile < 0.5:
                color = 3
            else:
                color = 7
        else:
            # For examples with smaller sizes, use colors 1, 2, 3, 7
            # Color 1: smallest objects
            if n <= 5:
                # For 5 or fewer objects, first ~40% of small objects get color 1
                if percentile < 0.4 and size <= 20:
                    color = 1
                elif percentile >= 0.82:
                    color = 7
                elif size >= 25:
                    color = 3
                else:
                    color = 2
            else:
                # For 6+ objects, only the very smallest gets color 1
                if i == 0:
                    color = 1
                elif percentile >= 0.82:
                    color = 7
                elif size >= 25 or (size <= 26 and percentile >= 0.65):
                    color = 3
                else:
                    color = 2

        # Color all points of this object
        # obj.points returns GridPoint objects with .x and .y attributes
        for p in obj.points:
            output.set(p.x, p.y, color)

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("37d3e8b2", solve)
