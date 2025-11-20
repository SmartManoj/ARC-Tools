import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task


def solve(grid: Grid):
    '''
    The grid is divided into a 3x3 grid of 3x3 blocks (separated by rows/columns of zeros).
    Sort the 9 blocks by the count of 1s in each block (ascending), maintaining their
    original reading order as a tie-breaker (stable sort). Then place the sorted blocks
    back into the grid in row-major order from bottom to top: positions (2,0), (2,1),
    (2,2), (1,0), (1,1), (1,2), (0,0), (0,1), (0,2).
    '''

    def extract_block(g, block_row, block_col):
        """Extract a 3x3 block from the grid"""
        row_start = block_row * 4
        col_start = block_col * 4
        block = []
        for r in range(3):
            row = []
            for c in range(3):
                row.append(g[row_start + r][col_start + c])
            block.append(row)
        return block

    def count_ones(block):
        """Count the number of 1s in a block"""
        return sum(row.count(1) for row in block)

    def place_block(g, block, block_row, block_col):
        """Place a 3x3 block into the grid"""
        row_start = block_row * 4
        col_start = block_col * 4
        for r in range(3):
            for c in range(3):
                g[row_start + r][col_start + c] = block[r][c]

    # Extract all 9 blocks in reading order (row-major: top-left to bottom-right)
    blocks = []
    for br in range(3):
        for bc in range(3):
            block = extract_block(grid, br, bc)
            blocks.append(block)

    # Sort blocks by count of 1s (stable sort preserves original order for ties)
    sorted_blocks = sorted(blocks, key=count_ones)

    # Create output grid (initialize with zeros)
    output_grid_data = [[0 for _ in range(grid.width)] for _ in range(grid.height)]
    output_grid = Grid(output_grid_data)

    # Place sorted blocks in row-major order from bottom to top
    # Positions: bottom-left, bottom-middle, bottom-right, middle-left, ...
    positions = [(2,0), (2,1), (2,2), (1,0), (1,1), (1,2), (0,0), (0,1), (0,2)]

    for i, pos in enumerate(positions):
        place_block(output_grid, sorted_blocks[i], pos[0], pos[1])

    return output_grid


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("dc2aa30b", solve)
