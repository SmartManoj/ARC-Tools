import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Tiles the input grid in a 3x3 arrangement with rotations.
    Creates a 9x9 output from a 3x3 input by placing rotated versions
    of the input in a specific pattern.
    '''
    h, w = len(grid), len(grid[0])
    result = Grid([[0] * (w * 3) for _ in range(h * 3)])

    # Helper to rotate grid 90 degrees clockwise
    def rotate_90(g):
        h, w = len(g), len(g[0])
        return [[g[h-1-c][r] for c in range(w)] for r in range(h)]

    # Helper to rotate 180 degrees
    def rotate_180(g):
        return [row[::-1] for row in g[::-1]]

    # Helper to rotate 270 degrees
    def rotate_270(g):
        return rotate_90(rotate_180(g))

    # Place the pattern in the 3x3 grid of tiles
    # Based on the examples, different rotations appear in different positions
    transformations = [
        [rotate_180, rotate_270, grid],
        [rotate_90, rotate_180, rotate_270],
        [rotate_90, rotate_180, grid]
    ]

    for tile_r in range(3):
        for tile_c in range(3):
            transform = transformations[tile_r][tile_c]
            transformed = transform(grid) if callable(transform) else transform
            for r in range(h):
                for c in range(w):
                    result[tile_r * h + r][tile_c * w + c] = transformed[r][c]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("8e2edd66", solve)
