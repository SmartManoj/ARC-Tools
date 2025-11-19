import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Template Stamping
    1. Extract the shape template (cells with value 1)
    2. Find color markers (non-zero, non-1 values)
    3. Determine if colors are arranged horizontally or vertically
    4. Replicate the template for each color:
       - Horizontal arrangement: stack shapes horizontally
       - Vertical arrangement: stack shapes vertically
    '''
    # Find the bounding box of the template (all cells with value 1)
    template_cells = []
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] == 1:
                template_cells.append((r, c))

    if not template_cells:
        return grid

    # Get bounding box of template
    min_r = min(r for r, c in template_cells)
    max_r = max(r for r, c in template_cells)
    min_c = min(c for r, c in template_cells)
    max_c = max(c for r, c in template_cells)

    template_height = max_r - min_r + 1
    template_width = max_c - min_c + 1

    # Extract the template shape (relative positions)
    template = []
    for r in range(template_height):
        row = []
        for c in range(template_width):
            if grid[min_r + r][min_c + c] == 1:
                row.append(True)
            else:
                row.append(False)
        template.append(row)

    # Find all color markers (non-zero, non-1 values)
    color_markers = []
    for r in range(grid.height):
        for c in range(grid.width):
            val = grid[r][c]
            if val != 0 and val != 1:
                color_markers.append((val, r, c))

    # Sort color markers by position to maintain order
    # Determine if arrangement is horizontal or vertical
    if len(color_markers) <= 1:
        # Single color or no colors
        colors = [m[0] for m in color_markers]
        is_horizontal = True
    else:
        # Check if colors are on same row (horizontal) or same column (vertical)
        rows = [m[1] for m in color_markers]
        cols = [m[2] for m in color_markers]

        if len(set(rows)) == 1:
            # All on same row - horizontal arrangement
            is_horizontal = True
            # Sort by column
            color_markers.sort(key=lambda x: x[2])
        else:
            # Vertical arrangement
            is_horizontal = False
            # Sort by row
            color_markers.sort(key=lambda x: x[1])

    colors = [m[0] for m in color_markers]

    # Create output grid
    if is_horizontal:
        # Stack horizontally
        output_height = template_height
        output_width = template_width * len(colors)
        output_data = [[0 for _ in range(output_width)] for _ in range(output_height)]

        for color_idx, color in enumerate(colors):
            col_offset = color_idx * template_width
            for r in range(template_height):
                for c in range(template_width):
                    if template[r][c]:
                        output_data[r][col_offset + c] = color
    else:
        # Stack vertically
        output_height = template_height * len(colors)
        output_width = template_width
        output_data = [[0 for _ in range(output_width)] for _ in range(output_height)]

        for color_idx, color in enumerate(colors):
            row_offset = color_idx * template_height
            for r in range(template_height):
                for c in range(template_width):
                    if template[r][c]:
                        output_data[row_offset + r][c] = color

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("12997ef3", solve)
