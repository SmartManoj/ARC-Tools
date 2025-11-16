import os
import numpy as np
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    The pattern: Grids have symmetric regions marked by 8s. The task is to extract
    the corresponding symmetric region and apply appropriate transformation.

    Steps:
    1. Find the rectangular region containing all 8s
    2. Determine which half of the grid the 8s are in (using center at col/row 15)
    3. Calculate the symmetric position:
       - Vertical mirror: col i → col (29 - i)
       - Horizontal mirror: row i → row (29 - i)
    4. Extract from symmetric position + offset of 2
    5. Apply transformation based on which dimensions were mirrored:
       - flip_lr (horizontal flip): when only columns changed (vertical reflection)
       - flip_ud (vertical flip): when only rows changed (horizontal reflection)
       - rot_180 (180° rotation): when both rows and cols changed (central reflection)
    '''
    # Convert to numpy array for easier manipulation
    # Grid can be accessed like a 2D array: grid[row][col]
    height_total = len(grid)
    width_total = len(grid[0]) if height_total > 0 else 0
    grid_array = np.array([[grid[r][c] for c in range(width_total)] for r in range(height_total)])

    # Find all positions with value 8
    eights_positions = np.where(grid_array == 8)

    if len(eights_positions[0]) == 0:
        # No 8s found, return empty grid or original grid
        return grid

    # Find bounding box of 8s region
    r1, r2 = eights_positions[0].min(), eights_positions[0].max()
    c1, c2 = eights_positions[1].min(), eights_positions[1].max()

    height = r2 - r1 + 1
    width = c2 - c1 + 1

    # Calculate symmetric positions (around grid center at row/col 14.5)
    # For a 30x30 grid (indices 0-29), position i mirrors to position (29 - i)
    sym_r1 = 29 - r2
    sym_r2 = 29 - r1
    sym_c1 = 29 - c2
    sym_c2 = 29 - c1

    # Determine extraction position and transformation based on which half the 8s are in
    # Use the center of the 8s region to determine which half it's in
    # Center threshold is at 15 (anything > 15 is considered right/bottom half)

    row_center = (r1 + r2) / 2
    col_center = (c1 + c2) / 2

    in_right_half = col_center > 15
    in_bottom_half = row_center > 15

    if in_right_half and in_bottom_half:
        # Central reflection: both rows and cols change
        ext_r1 = sym_r1 + 2
        ext_r2 = ext_r1 + height - 1
        ext_c1 = sym_c1 + 2
        ext_c2 = ext_c1 + width - 1
        transform = "rot_180"
    elif in_right_half:
        # Vertical reflection: only cols change, rows stay the same
        ext_r1 = r1
        ext_r2 = r2
        ext_c1 = sym_c1 + 2
        ext_c2 = ext_c1 + width - 1
        transform = "flip_lr"
    elif in_bottom_half:
        # Horizontal reflection: only rows change, cols stay the same
        ext_r1 = sym_r1 + 2
        ext_r2 = ext_r1 + height - 1
        ext_c1 = c1
        ext_c2 = c2
        transform = "flip_ud"
    else:
        # 8s are in top-left quadrant - shouldn't happen based on examples
        # Default to original region
        ext_r1, ext_r2 = r1, r2
        ext_c1, ext_c2 = c1, c2
        transform = "original"

    # Extract the region
    extracted = grid_array[ext_r1:ext_r2+1, ext_c1:ext_c2+1]

    # Apply transformation
    if transform == "flip_lr":
        result = np.fliplr(extracted)
    elif transform == "flip_ud":
        result = np.flipud(extracted)
    elif transform == "rot_180":
        result = np.rot90(extracted, 2)  # 180 degree rotation
    else:
        result = extracted

    # Convert back to Grid
    return Grid(result.tolist())


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("0934a4d8", solve)
