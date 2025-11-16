import os
from arc_tools.grid import Grid, detect_objects
from arc_tools import logger

def extract_shape_pattern(obj):
    """Extract the normalized shape pattern from an object.
    Returns a tuple representing the shape where 1 = foreground, 0 = background.
    """
    pattern = []
    for row in range(obj.height):
        row_pattern = []
        for col in range(obj.width):
            val = obj[row][col]
            # Normalize: 1 for foreground (non-background), 0 for background
            row_pattern.append(1 if val != obj.background_color else 0)
        pattern.append(tuple(row_pattern))
    return tuple(pattern)

def get_object_color(obj):
    """Get the primary foreground color from an object."""
    for row in range(obj.height):
        for col in range(obj.width):
            val = obj[row][col]
            if val != obj.background_color:
                return val
    return None

def solve_2a5f8217(grid: Grid) -> Grid:
    """
    Pattern: Find blue (color 1) shapes and replace them with matching colored shapes.

    For each blue (1) shape:
    1. Extract its pattern
    2. Find a non-blue shape with the same pattern
    3. Replace the blue shape with the color of the matching shape
    """
    result = grid.copy()

    # Find all unique colors in the grid (excluding background and blue)
    all_colors = set()
    for row in range(grid.height):
        for col in range(grid.width):
            color = grid[row][col]
            if color != 0 and color != 1:  # Not background, not blue
                all_colors.add(color)

    # For each color, create a mask and detect objects of that color
    template_objects = []
    for target_color in all_colors:
        # Create a grid with only this color
        color_grid = Grid([[target_color if cell == target_color else 0
                           for cell in row]
                          for row in grid])
        # Detect objects in this color-specific grid
        color_objs = detect_objects(color_grid)
        for obj in color_objs:
            template_objects.append((obj, target_color))

    # Similarly, create a grid with only blue objects
    blue_grid = Grid([[1 if cell == 1 else 0 for cell in row] for row in grid])
    blue_objects = detect_objects(blue_grid)

    # For each blue object, find matching template and replace
    for blue_obj in blue_objects:
        blue_pattern = extract_shape_pattern(blue_obj)

        # Find matching template
        for template_obj, template_color in template_objects:
            template_pattern = extract_shape_pattern(template_obj)

            if blue_pattern == template_pattern:
                # Found a match! Replace blue with template color
                # Replace all blue pixels in this object with the new color
                for y in range(blue_obj.height):
                    for x in range(blue_obj.width):
                        if blue_obj[y][x] == 1:  # Blue pixel
                            grid_y = blue_obj.region.y1 + y
                            grid_x = blue_obj.region.x1 + x
                            result[grid_y][grid_x] = template_color

                break  # Found the match, move to next blue object

    return result

if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/home/user/ARC-Tools')
    from evaluation_tasks_v1.helper import solve_task
    solve_task('2a5f8217', solve_2a5f8217)
