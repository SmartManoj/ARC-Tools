import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms input grid into output by creating a 2x2 arrangement of flipped versions.

    Pattern: The output is composed of 4 quadrants (each the same size as input):
    - Top-Left (TL): Input rotated 180° (flipped both vertically and horizontally)
    - Top-Right (TR): Input flipped vertically (upside down)
    - Bottom-Left (BL): Input flipped horizontally (left-right)
    - Bottom-Right (BR): Original input

    Layout:
    [180° rotation] | [vertical flip]
    ----------------+----------------
    [horizontal flip] | [original]
    '''
    height = grid.height
    width = grid.width

    # Create the 4 quadrants
    # BR (bottom-right): Original input
    original = [[grid[r][c] for c in range(width)] for r in range(height)]

    # TR (top-right): Vertical flip (upside down)
    vertical_flip = [[grid[r][c] for c in range(width)] for r in range(height-1, -1, -1)]

    # BL (bottom-left): Horizontal flip (left-right)
    horizontal_flip = [[grid[r][c] for c in range(width-1, -1, -1)] for r in range(height)]

    # TL (top-left): 180° rotation (both flips)
    rotation_180 = [[grid[r][c] for c in range(width-1, -1, -1)] for r in range(height-1, -1, -1)]

    # Construct output: combine quadrants
    output_data = []

    # Top half: TL | TR (concatenate horizontally)
    for i in range(height):
        output_data.append(rotation_180[i] + vertical_flip[i])

    # Bottom half: BL | BR (concatenate horizontally)
    for i in range(height):
        output_data.append(horizontal_flip[i] + original[i])

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("0c786b71", solve)
