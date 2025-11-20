import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transform rectangles filled with 8s into multi-colored regions.
    Each rectangle is divided into quadrants:
    - Top-left quarter: Color 6 (magenta)
    - Top-right quarter: Color 1 (blue)
    - Bottom-left quarter: Color 2 (red)
    - Bottom-right quarter: Color 3 (green)
    - Center region: Color 4 (yellow)
    '''
    objects = detect_objects(grid)
    result = Grid([[grid[r][c] for c in range(len(grid[0]))] for r in range(len(grid))])

    for obj in objects:
        if obj.color == Color.LIGHT_BLUE.value:  # Color 8
            height = obj.height
            width = obj.width

            # Calculate quarter boundaries
            top_quarter = height // 4
            bottom_quarter = height // 4
            # Left and right edges in middle rows are always 2 columns
            left_quarter = 2
            right_quarter = 2

            # Process each cell in the rectangle
            for r in range(height):
                for c in range(width):
                    # Determine the color based on position
                    if r < top_quarter:  # Top quarter rows
                        # Split horizontally in half
                        if c < width // 2:
                            color = Color.MAGENTA.value  # 6
                        else:
                            color = Color.BLUE.value  # 1
                    elif r >= height - bottom_quarter:  # Bottom quarter rows
                        # Split horizontally in half
                        if c < width // 2:
                            color = Color.RED.value  # 2
                        else:
                            color = Color.GREEN.value  # 3
                    else:  # Middle rows
                        if c < left_quarter:  # Left quarter columns
                            # Split vertically (top or bottom half of rectangle)
                            if r < height // 2:
                                color = Color.MAGENTA.value  # 6
                            else:
                                color = Color.RED.value  # 2
                        elif c >= width - right_quarter:  # Right quarter columns
                            # Split vertically (top or bottom half of rectangle)
                            if r < height // 2:
                                color = Color.BLUE.value  # 1
                            else:
                                color = Color.GREEN.value  # 3
                        else:  # Middle columns
                            color = Color.YELLOW.value  # 4

                    # Set the color in the result grid (region uses x=col, y=row)
                    result[obj.region.y1 + r][obj.region.x1 + c] = color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("639f5a19", solve)
