import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms a 3x9 grid into a 3x9 grid by:
    1. Dividing the input into three 3x3 blocks
    2. Identifying the pattern in each block
    3. Replacing each block with a solid color based on the pattern

    Pattern mappings:
    - Frame/hollow square [[5,5,5], [5,0,5], [5,5,5]] -> color 3
    - Center dot [[0,0,0], [0,5,0], [0,0,0]] -> color 4
    - Diagonal (top-right to bottom-left) [[0,0,5], [0,5,0], [5,0,0]] -> color 9
    - Bottom horizontal [[0,0,0], [0,0,0], [5,5,5]] -> color 1
    - Top horizontal [[5,5,5], [0,0,0], [0,0,0]] -> color 6
    '''

    def identify_pattern(block):
        """Identify the pattern in a 3x3 block and return the corresponding color"""
        # Frame pattern (hollow square)
        if (block[0] == [5, 5, 5] and
            block[1] == [5, 0, 5] and
            block[2] == [5, 5, 5]):
            return 3

        # Center dot
        if (block[0] == [0, 0, 0] and
            block[1] == [0, 5, 0] and
            block[2] == [0, 0, 0]):
            return 4

        # Diagonal (top-right to bottom-left)
        if (block[0] == [0, 0, 5] and
            block[1] == [0, 5, 0] and
            block[2] == [5, 0, 0]):
            return 9

        # Bottom horizontal
        if (block[0] == [0, 0, 0] and
            block[1] == [0, 0, 0] and
            block[2] == [5, 5, 5]):
            return 1

        # Top horizontal
        if (block[0] == [5, 5, 5] and
            block[1] == [0, 0, 0] and
            block[2] == [0, 0, 0]):
            return 6

        # If no pattern matches, return 0 (should not happen in valid inputs)
        return 0

    # Initialize output grid
    output_data = []

    # Process each row
    for row_idx in range(3):
        output_row = []

        # Process each 3x3 block (there are 3 blocks per row)
        for block_idx in range(3):
            start_col = block_idx * 3
            end_col = start_col + 3

            # Extract the 3x3 block
            block = []
            for r in range(3):
                block.append(grid[r][start_col:end_col])

            # Identify the pattern and get the color
            color = identify_pattern(block)

            # Fill the output with the solid color (3 cells for this block's portion of the row)
            output_row.extend([color, color, color])

        output_data.append(output_row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("17cae0c1", solve)
