import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern Analysis:
    1. There's a green (5) rectangle in the grid that acts as a "legend"
    2. The green rectangle contains colored markers (non-0, non-5 pixels)
    3. There are shapes in the grid made of a specific color (8 or 1 in examples)
    4. Each shape should be recolored based on the nearest marker in the green rectangle

    Algorithm:
    1. Find all non-zero, non-green colored markers (these are the target colors)
    2. Detect all objects/shapes that need to be recolored
    3. For each shape, find the nearest marker and recolor it with that marker's color
    '''

    # Create a copy of the grid
    output = Grid([[grid[r][c] for c in range(grid.width)] for r in range(grid.height)])

    # Step 1: Find all colored markers (non-0, non-5 colors and their positions)
    markers = []
    shape_color = None

    for r in range(grid.height):
        for c in range(grid.width):
            color = grid[r][c]
            if color != 0 and color != 5:
                # Check if this is a marker (surrounded by or near green/black)
                # or if it's part of a shape
                neighbors_green = False
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < grid.height and 0 <= nc < grid.width:
                        if grid[nr][nc] == 5:
                            neighbors_green = True
                            break

                if neighbors_green:
                    # This is a marker
                    markers.append((r, c, color))
                else:
                    # This might be the shape color
                    if shape_color is None:
                        shape_color = color

    # Sort markers by row position (top to bottom), then by column
    markers.sort(key=lambda m: (m[0], m[1]))
    logger.info(f"Found {len(markers)} markers (sorted): {markers}")
    logger.info(f"Shape color: {shape_color}")

    # Step 2: Detect all objects of the shape color
    objects = detect_objects(grid, ignore_colors=[0, 5], single_color_only=True)

    # Filter to only objects with the shape color
    shape_objects = [obj for obj in objects if len(obj.points) > 0 and grid[obj.points[0].y][obj.points[0].x] == shape_color]

    # Sort shapes by their vertical center position (top to bottom)
    shape_objects_with_centers = []
    for obj in shape_objects:
        avg_r = sum(p.y for p in obj.points) / len(obj.points)
        avg_c = sum(p.x for p in obj.points) / len(obj.points)
        shape_objects_with_centers.append((obj, avg_r, avg_c))

    shape_objects_with_centers.sort(key=lambda x: x[1])  # Sort by avg_r (row)

    logger.info(f"Found {len(shape_objects_with_centers)} shapes to recolor")

    # Step 3: Match shapes to markers by their vertical order
    for i, (obj, avg_r, avg_c) in enumerate(shape_objects_with_centers):
        if i < len(markers):
            marker_r, marker_c, marker_color = markers[i]
            logger.info(f"Shape {i+1} at ({avg_r:.1f}, {avg_c:.1f}) -> marker {i+1} at ({marker_r}, {marker_c}) color {marker_color}")

            # Recolor the shape
            for p in obj.points:
                if grid[p.y][p.x] == shape_color:
                    output[p.y][p.x] = marker_color
        else:
            logger.warning(f"Shape {i+1} has no corresponding marker!")

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("1da012fc", solve)
