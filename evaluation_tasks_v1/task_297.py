import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Create a 9x9 tiled pattern from a 3x3 input with rotations.
    The input is rotated and tiled to create a larger symmetric pattern.
    '''
    # Output is 9x9 (3x3 tiles of 3x3 each)
    result = Grid.empty(9, 9)

    # Create rotations of the input
    def rotate_180(g):
        rotated = Grid.empty(g.height, g.width)
        for r in range(g.height):
            for c in range(g.width):
                rotated[r, c] = g[g.height - 1 - r, g.width - 1 - c]
        return rotated

    def flip_horizontal(g):
        flipped = Grid.empty(g.height, g.width)
        for r in range(g.height):
            for c in range(g.width):
                flipped[r, c] = g[r, g.width - 1 - c]
        return flipped

    # Create variations
    grid_normal = grid
    grid_flipped = flip_horizontal(grid)
    grid_rotated = rotate_180(grid)

    # Tile the 9x9 output
    # Row 0: rotated, rotated, rotated
    # Row 1: flipped, normal, flipped
    # Row 2: flipped, normal, flipped (repeat)
    for tile_r in range(3):
        for tile_c in range(3):
            if tile_r == 0:
                source = grid_rotated
            elif tile_c == 1:
                source = grid_normal
            else:
                source = grid_flipped

            # Copy the tile
            for r in range(3):
                for c in range(3):
                    result[tile_r * 3 + r, tile_c * 3 + c] = source[r, c]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("c48954c1", solve)
