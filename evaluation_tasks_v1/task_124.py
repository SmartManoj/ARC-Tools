import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern:
    1. Find all marker cells (non-zero, non-6 values)
    2. Detect connected components of 6s
    3. For each component, find the closest marker
    4. Extract bounding box and replace 6s with marker color
    5. Arrange extracted shapes horizontally or vertically based on marker positions
    '''

    # Find all markers (non-zero, non-6 cells)
    markers = []
    for y in range(grid.height):
        for x in range(grid.width):
            value = grid[y][x]
            if value != 0 and value != 6:
                markers.append((x, y, value))

    # Detect all objects (connected components of 6s)
    objects = detect_objects(grid, required_colors=[6], go_diagonal=False)

    # For each marker, find the closest 6-object
    marker_to_object = {}
    for mx, my, color in markers:
        min_dist = float('inf')
        closest_obj = None

        for obj in objects:
            # Calculate minimum distance from marker to any cell in object
            for point in obj.points:
                obj_x = point.x
                obj_y = point.y
                dist = abs(mx - obj_x) + abs(my - obj_y)
                if dist < min_dist:
                    min_dist = dist
                    closest_obj = obj

        if closest_obj:
            marker_to_object[(mx, my, color)] = closest_obj

    # Extract and recolor each component
    transformed_shapes = []
    for (mx, my, color), obj in marker_to_object.items():
        # Get bounding box
        min_x = min(point.x for point in obj.points)
        max_x = max(point.x for point in obj.points)
        min_y = min(point.y for point in obj.points)
        max_y = max(point.y for point in obj.points)

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        # Create the transformed shape
        shape_data = [[0 for _ in range(width)] for _ in range(height)]
        for point in obj.points:
            rel_x = point.x - min_x
            rel_y = point.y - min_y
            shape_data[rel_y][rel_x] = color

        transformed_shapes.append({
            'data': shape_data,
            'marker_pos': (mx, my),
            'color': color,
            'height': height,
            'width': width
        })

    # Sort shapes by marker position
    # Determine if we should arrange horizontally or vertically
    # If markers are in similar row (vertical variation < horizontal), arrange horizontally
    # Otherwise, arrange vertically

    if len(transformed_shapes) == 0:
        return Grid([[0]])

    marker_cols = [s['marker_pos'][0] for s in transformed_shapes]
    marker_rows = [s['marker_pos'][1] for s in transformed_shapes]

    col_range = max(marker_cols) - min(marker_cols)
    row_range = max(marker_rows) - min(marker_rows)

    # Sort by row first, then column
    transformed_shapes.sort(key=lambda s: (s['marker_pos'][1], s['marker_pos'][0]))

    if col_range > row_range:
        # Arrange horizontally (sort by column)
        transformed_shapes.sort(key=lambda s: (s['marker_pos'][0], s['marker_pos'][1]))

        # Find max height
        max_height = max(s['height'] for s in transformed_shapes)
        total_width = sum(s['width'] for s in transformed_shapes)

        # Create output grid
        output_data = [[0 for _ in range(total_width)] for _ in range(max_height)]

        current_x = 0
        for shape in transformed_shapes:
            for y in range(shape['height']):
                for x in range(shape['width']):
                    output_data[y][current_x + x] = shape['data'][y][x]
            current_x += shape['width']
    else:
        # Arrange vertically (sort by row)
        transformed_shapes.sort(key=lambda s: (s['marker_pos'][1], s['marker_pos'][0]))

        # Find max width
        max_width = max(s['width'] for s in transformed_shapes)
        total_height = sum(s['height'] for s in transformed_shapes)

        # Create output grid
        output_data = [[0 for _ in range(max_width)] for _ in range(total_height)]

        current_y = 0
        for shape in transformed_shapes:
            for y in range(shape['height']):
                for x in range(shape['width']):
                    output_data[current_y + y][x] = shape['data'][y][x]
            current_y += shape['height']

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("50aad11f", solve)
