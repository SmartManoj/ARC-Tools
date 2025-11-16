import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    For each object (connected non-zero region) that contains exactly 2 colors,
    swap those two colors.

    Example:
    - If an object has colors 8 and 4, all cells with 8 become 4 and vice versa
    - If an object has colors 3 and 2, all cells with 3 become 2 and vice versa
    '''
    # Create a copy of the grid to modify
    output_data = [[grid[row][col] for col in range(grid.width)] for row in range(grid.height)]

    # Detect all objects (connected regions of non-zero cells)
    objects = detect_objects(grid, go_diagonal=True)

    for obj in objects:
        # Get unique colors in this object (excluding background)
        unique_colors = set()
        for point in obj.points:
            color = grid[point.y][point.x]
            if color != grid.background_color:
                unique_colors.add(color)

        # If exactly 2 colors, swap them
        if len(unique_colors) == 2:
            color1, color2 = list(unique_colors)

            # Swap colors for all points in this object
            for point in obj.points:
                current_color = grid[point.y][point.x]
                if current_color == color1:
                    output_data[point.y][point.x] = color2
                elif current_color == color2:
                    output_data[point.y][point.x] = color1

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("45737921", solve)
