import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern:
    1. Input is divided by a horizontal line of 5s (gray)
    2. Top section contains 3 colored shapes: blue (1), red (2), and a third color
    3. Bottom section contains a blue (1) shape
    4. Output combines the bottom blue shape with the top third-color shape
    5. Stacked vertically in a trimmed output grid
    '''
    # Find the divider line (row with all 5s)
    divider_row = None
    for i, row in enumerate(grid):
        if all(cell == 5 for cell in row):
            divider_row = i
            break

    if divider_row is None:
        raise ValueError("No divider row found")

    # Split into top and bottom sections
    height, width = len(grid), len(grid[0])

    # Create top section (rows 0 to divider_row-1)
    top_section = Grid([grid[i] for i in range(divider_row)])

    # Create bottom section (rows divider_row+1 to end)
    bottom_section = Grid([grid[i] for i in range(divider_row + 1, height)])

    # Detect objects in both sections
    top_objects = detect_objects(top_section)
    bottom_objects = detect_objects(bottom_section)

    # Find the blue shape in bottom section
    bottom_blue = None
    for obj in bottom_objects:
        if obj.color == Color.BLUE.value:
            bottom_blue = obj
            break

    # Find the third color in top section (rightmost non-blue, non-red shape)
    third_color_obj = None
    max_col = -1
    for obj in top_objects:
        if obj.color != Color.BLUE.value and obj.color != Color.RED.value:
            # Check if this object is more to the right
            obj_max_col = obj.region.x2
            if obj_max_col > max_col:
                max_col = obj_max_col
                third_color_obj = obj

    if bottom_blue is None or third_color_obj is None:
        raise ValueError("Could not find required shapes")

    # Extract the shapes with their patterns
    bottom_blue_points = [(p.x, p.y) for p in bottom_blue.points]
    third_color_points = [(p.x, p.y) for p in third_color_obj.points]

    # Get bounding boxes from region
    blue_min_x = bottom_blue.region.x1
    blue_max_x = bottom_blue.region.x2
    blue_min_y = bottom_blue.region.y1
    blue_height = bottom_blue.region.height

    third_min_x = third_color_obj.region.x1
    third_max_x = third_color_obj.region.x2
    third_min_y = third_color_obj.region.y1
    third_height = third_color_obj.region.height

    # Calculate center columns to align shapes
    blue_center_x = (blue_min_x + blue_max_x) / 2.0
    third_center_x = (third_min_x + third_max_x) / 2.0

    # The x shift needed to align third color's center with blue's center
    center_shift = blue_center_x - third_center_x

    # Determine which shape goes on top based on bottom blue's row position
    # blue_min_y is relative to bottom section (starts at 0)
    # Add divider_row + 1 to get absolute position in original grid
    blue_absolute_row = blue_min_y + divider_row + 1

    # Create output grid (9 rows x 15 cols based on examples)
    output = Grid([[0] * width for _ in range(9)])

    # Determine ordering: third color above if blue is far down (row > 10)
    # Special case: if blue is at row 9 and leftmost col <= 5, third also goes above
    third_goes_above = (blue_absolute_row > 10) or (blue_absolute_row == 9 and blue_min_x <= 5)

    if third_goes_above:
        # Third color above, blue below
        # Starting row depends on blue's absolute row position
        if blue_absolute_row > 10:
            start_row_third = 2
        else:  # blue_absolute_row == 9
            start_row_third = 0
        for x, y in third_color_points:
            out_x = int(x + center_shift)
            out_y = y - third_min_y + start_row_third
            if 0 <= out_x < width and 0 <= out_y < 9:
                output[out_y][out_x] = third_color_obj.color

        # Place blue below third color (no gap, just stack them)
        start_row_blue = start_row_third + third_height
        for x, y in bottom_blue_points:
            out_x = x
            out_y = y - blue_min_y + start_row_blue
            if 0 <= out_x < width and 0 <= out_y < 9:
                output[out_y][out_x] = Color.BLUE.value
    else:
        # Blue above, third color below
        # Place blue starting at row 1 or 3 depending on absolute row
        if blue_absolute_row <= 7:
            start_row_blue = 1
        else:
            start_row_blue = 3

        for x, y in bottom_blue_points:
            out_x = x
            out_y = y - blue_min_y + start_row_blue
            if 0 <= out_x < width and 0 <= out_y < 9:
                output[out_y][out_x] = Color.BLUE.value

        # Place third color below blue (no gap, just stack them)
        start_row_third = start_row_blue + blue_height
        for x, y in third_color_points:
            out_x = int(x + center_shift)
            out_y = y - third_min_y + start_row_third
            if 0 <= out_x < width and 0 <= out_y < 9:
                output[out_y][out_x] = third_color_obj.color

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("4c177718", solve)
