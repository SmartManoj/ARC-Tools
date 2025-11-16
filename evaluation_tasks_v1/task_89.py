import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task
from collections import Counter

def solve(grid: Grid):
    '''
    Pattern: Find all 5x5 blocks of colored cells, then return the block
    that has the rarest number of zeros (background cells) among all blocks.

    Algorithm:
    1. Scan the input grid for all 5x5 regions that contain mostly colored cells
    2. For each 5x5 block found, count how many zeros (background) it contains
    3. Find which zero count appears least frequently among all blocks
    4. Return the block with that rarest zero count
    '''

    # Find all 5x5 blocks that contain mostly colored cells
    blocks = []
    zero_counts = []

    height = len(grid)
    width = len(grid[0])

    for r in range(height - 4):
        for c in range(width - 4):
            # Extract 5x5 block
            block = []
            color_count = 0

            for i in range(5):
                row = []
                for j in range(5):
                    val = grid[r + i][c + j]
                    row.append(val)
                    if val != 0:
                        color_count += 1
                block.append(row)

            # Keep blocks that have at least 20 colored cells (out of 25)
            if color_count >= 20:
                zero_count = 25 - color_count
                blocks.append(block)
                zero_counts.append(zero_count)

    # Find the zero count that appears least frequently
    count_freq = Counter(zero_counts)
    rarest_zero_count = min(count_freq, key=count_freq.get)

    # Find the index of the block with the rarest zero count
    rarest_idx = zero_counts.index(rarest_zero_count)

    # Return that block as a Grid
    return Grid(blocks[rarest_idx])

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("358ba94e", solve)
