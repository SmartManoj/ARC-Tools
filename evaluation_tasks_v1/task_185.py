import os
from arc_tools.grid import Grid
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task


def solve(grid: Grid):
    '''
    Create an 8x8 output grid from a 4x4 input grid by arranging four rotations:
    - Top-left: Original
    - Top-right: 90 degrees counter-clockwise
    - Bottom-left: 180 degrees
    - Bottom-right: 90 degrees clockwise
    '''
    h, w = grid.height, grid.width

    # Create 8x8 output grid
    output = Grid([[0] * 8 for _ in range(8)])

    # Helper functions for rotations
    def rotate_90_cw(grid_data):
        """Rotate 90 degrees clockwise"""
        h, w = len(grid_data), len(grid_data[0])
        rotated = [[0] * h for _ in range(w)]
        for i in range(h):
            for j in range(w):
                rotated[j][h - 1 - i] = grid_data[i][j]
        return rotated

    def rotate_90_ccw(grid_data):
        """Rotate 90 degrees counter-clockwise"""
        h, w = len(grid_data), len(grid_data[0])
        rotated = [[0] * h for _ in range(w)]
        for i in range(h):
            for j in range(w):
                rotated[h - 1 - j][i] = grid_data[i][j]
        return rotated

    def rotate_180(grid_data):
        """Rotate 180 degrees"""
        h, w = len(grid_data), len(grid_data[0])
        rotated = [[0] * w for _ in range(h)]
        for i in range(h):
            for j in range(w):
                rotated[h - 1 - i][w - 1 - j] = grid_data[i][j]
        return rotated

    # Get grid as 2D list
    grid_data = [list(grid[i]) for i in range(h)]

    # Compute rotations
    rot_cw = rotate_90_cw(grid_data)
    rot_ccw = rotate_90_ccw(grid_data)
    rot_180 = rotate_180(grid_data)

    # Place quadrants in output
    # Top-left: Original
    for i in range(h):
        for j in range(w):
            output[i][j] = grid_data[i][j]

    # Top-right: 90 CCW
    for i in range(h):
        for j in range(w):
            output[i][j + w] = rot_ccw[i][j]

    # Bottom-left: 180
    for i in range(h):
        for j in range(w):
            output[i + h][j] = rot_180[i][j]

    # Bottom-right: 90 CW
    for i in range(h):
        for j in range(w):
            output[i + h][j + w] = rot_cw[i][j]

    return output


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("7953d61e", solve)
