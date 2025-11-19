import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Identifies L-shaped markers (color 7) and uses their orientation to determine
    what color to replace nearby regions (color 1) with. The markers are then cleared.

    L-shape orientations map to colors:
    - Upper-left L (0 7 / 7 7) → color 3
    - Upper-right L (7 7 / 7 0) → color 6
    - Lower-right L (7 7 / 0 7) → color 4
    - Lower-left L (7 0 / 7 7) → color 8
    '''
    # Create output grid
    output_grid = [[grid[y][x] for x in range(grid.width)] for y in range(grid.height)]

    # Detect all objects of color 7 (markers) and color 1 (targets)
    markers = detect_objects(grid, required_colors=[7])
    targets = detect_objects(grid, required_colors=[1])

    # Process each marker
    for marker in markers:
        # Get marker cells and determine its shape
        marker_cells = [(p.x, p.y) for p in marker.points]

        # Normalize to bounding box
        min_x = min(p.x for p in marker.points)
        min_y = min(p.y for p in marker.points)
        max_x = max(p.x for p in marker.points)
        max_y = max(p.y for p in marker.points)

        # Create normalized pattern (should be 2x2 with 3 cells)
        pattern = [[0, 0], [0, 0]]
        for p in marker.points:
            rel_x = p.x - min_x
            rel_y = p.y - min_y
            if rel_y < 2 and rel_x < 2:
                pattern[rel_y][rel_x] = 7

        # Determine color based on L-shape orientation
        target_color = None
        if pattern == [[0, 7], [7, 7]]:  # Upper-left L
            target_color = 3
        elif pattern == [[7, 7], [7, 0]]:  # Upper-right L
            target_color = 6
        elif pattern == [[7, 7], [0, 7]]:  # Lower-right L
            target_color = 4
        elif pattern == [[7, 0], [7, 7]]:  # Lower-left L
            target_color = 8
        else:
            logger.info(f"Unknown marker pattern: {pattern}")
            target_color = 3  # Default fallback

        # Find the nearest target region (color 1)
        marker_center_x = (min_x + max_x) / 2
        marker_center_y = (min_y + max_y) / 2

        nearest_target = None
        min_distance = float('inf')

        for target in targets:
            # Calculate center of target
            target_min_x = min(p.x for p in target.points)
            target_max_x = max(p.x for p in target.points)
            target_min_y = min(p.y for p in target.points)
            target_max_y = max(p.y for p in target.points)
            target_center_x = (target_min_x + target_max_x) / 2
            target_center_y = (target_min_y + target_max_y) / 2

            # Calculate distance
            distance = ((marker_center_x - target_center_x) ** 2 +
                       (marker_center_y - target_center_y) ** 2) ** 0.5

            if distance < min_distance:
                min_distance = distance
                nearest_target = target

        # Recolor the nearest target
        if nearest_target:
            for p in nearest_target.points:
                output_grid[p.y][p.x] = target_color

        # Clear the marker
        for x, y in marker_cells:
            output_grid[y][x] = 0

    return Grid(output_grid)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("604001fa", solve)
