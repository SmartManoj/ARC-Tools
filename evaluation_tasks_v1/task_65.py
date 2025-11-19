import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task
import numpy as np

def solve(grid: Grid):
    '''
    Pattern:
    1. Extract the bounding box of non-zero values from the input
    2. Create four transformations of the shape:
       - Original shape
       - Horizontal flip (mirror left-right)
       - Transpose (swap rows and columns)
       - Vertical flip of transpose
    3. Create output grid with size = 2*max(height,width) + min(height,width)
    4. Place the transformations in a cross pattern:
       - Top center: transpose
       - Left middle: original
       - Right middle: horizontal flip
       - Bottom center: vertical flip of transpose
    '''
    # Convert to numpy array for easier manipulation
    data = np.array([[grid[r][c] for c in range(len(grid[0]))] for r in range(len(grid))])

    # Find bounding box of non-zero values
    rows, cols = np.where(data != 0)

    if len(rows) == 0:
        return grid

    min_r, max_r = rows.min(), rows.max()
    min_c, max_c = cols.min(), cols.max()

    # Extract shape
    shape = data[min_r:max_r+1, min_c:max_c+1]
    shape_h, shape_w = shape.shape

    # Create transformations
    h_flip = np.fliplr(shape)  # Horizontal flip
    transpose = shape.T  # Transpose
    v_flip_transpose = np.flipud(transpose)  # Vertical flip of transpose

    # Calculate output dimensions
    max_dim = max(shape_h, shape_w)
    min_dim = min(shape_h, shape_w)
    output_size = 2 * max_dim + min_dim

    # Create output grid
    output = np.zeros((output_size, output_size), dtype=int)

    # Place transformations:
    # Top center: transpose (max_dim x min_dim)
    output[0:max_dim, max_dim:max_dim+min_dim] = transpose

    # Left middle: original (min_dim x max_dim)
    output[max_dim:max_dim+min_dim, 0:max_dim] = shape

    # Right middle: horizontal flip (min_dim x max_dim)
    output[max_dim:max_dim+min_dim, max_dim+min_dim:2*max_dim+min_dim] = h_flip

    # Bottom center: vertical flip of transpose (max_dim x min_dim)
    output[max_dim+min_dim:2*max_dim+min_dim, max_dim:max_dim+min_dim] = v_flip_transpose

    return Grid(output.tolist())

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("2697da3f", solve)
