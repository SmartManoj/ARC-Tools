import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    Pattern: Find a nested rectangle structure (outer color surrounding inner color)
    and add a border around the entire structure using the inner color.

    Border thickness rules:
    - If inner rectangle is square: border thickness = side length of inner square
    - If inner rectangle is non-square: border thickness = frame thickness of outer color
    '''
    # Find all non-zero colors in the grid
    colors = set()
    for row in grid:
        for cell in row:
            if cell != 0:
                colors.add(cell)

    if len(colors) < 2:
        # Need at least 2 colors for nested structure
        return grid

    # Find bounding boxes for each color
    color_bounds = {}
    for color in colors:
        min_row, max_row = float('inf'), -1
        min_col, max_col = float('inf'), -1
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == color:
                    min_row = min(min_row, r)
                    max_row = max(max_row, r)
                    min_col = min(min_col, c)
                    max_col = max(max_col, c)
        if max_row >= 0:
            color_bounds[color] = (min_row, max_row, min_col, max_col)

    # Identify outer and inner colors based on bounding box sizes
    color_areas = {color: (bounds[1] - bounds[0] + 1) * (bounds[3] - bounds[2] + 1)
                   for color, bounds in color_bounds.items()}
    outer_color = max(color_areas, key=color_areas.get)
    inner_color = min(color_areas, key=color_areas.get)

    outer_bounds = color_bounds[outer_color]
    inner_bounds = color_bounds[inner_color]

    # Calculate dimensions
    inner_height = inner_bounds[1] - inner_bounds[0] + 1
    inner_width = inner_bounds[3] - inner_bounds[2] + 1

    # Determine border thickness
    if inner_height == inner_width:
        # Square inner: border thickness = side length
        border_thickness = inner_height
    else:
        # Non-square inner: border thickness = frame thickness of outer color
        frame_top = inner_bounds[0] - outer_bounds[0]
        frame_bottom = outer_bounds[1] - inner_bounds[1]
        frame_left = inner_bounds[2] - outer_bounds[2]
        frame_right = outer_bounds[3] - inner_bounds[3]
        # Use the most common frame thickness
        border_thickness = max(frame_top, frame_bottom, frame_left, frame_right)

    # Find the overall bounding box of the structure
    struct_min_row = outer_bounds[0]
    struct_max_row = outer_bounds[1]
    struct_min_col = outer_bounds[2]
    struct_max_col = outer_bounds[3]

    # Create output grid
    height = len(grid)
    width = len(grid[0])
    output = [[0 for _ in range(width)] for _ in range(height)]

    # Copy original structure
    for r in range(height):
        for c in range(width):
            output[r][c] = grid[r][c]

    # Add border around the structure
    new_min_row = max(0, struct_min_row - border_thickness)
    new_max_row = min(height - 1, struct_max_row + border_thickness)
    new_min_col = max(0, struct_min_col - border_thickness)
    new_max_col = min(width - 1, struct_max_col + border_thickness)

    # Fill the border with inner color
    for r in range(new_min_row, new_max_row + 1):
        for c in range(new_min_col, new_max_col + 1):
            # Only fill if it's in the border area (not already part of structure)
            if (r < struct_min_row or r > struct_max_row or
                c < struct_min_col or c > struct_max_col):
                output[r][c] = inner_color

    return Grid(output)


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("3a301edc", solve)
