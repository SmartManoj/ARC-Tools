import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    Find the 2x2 seed pattern and expand it in a fractal pattern.
    The seed values fill regions based on a staircase expansion rule.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find the 2x2 seed (non-zero values)
    seed_row, seed_col = None, None
    seed_values = None

    for r in range(h - 1):
        for c in range(w - 1):
            # Check if we have a 2x2 block of non-zero values
            tl = grid[r][c]
            tr = grid[r][c + 1]
            bl = grid[r + 1][c]
            br = grid[r + 1][c + 1]

            if tl != 0 and tr != 0 and bl != 0 and br != 0:
                seed_row, seed_col = r, c
                seed_values = [[tl, tr], [bl, br]]
                break
        if seed_values:
            break

    if not seed_values:
        return result

    tl, tr = seed_values[0]
    bl, br = seed_values[1]

    def get_fill_start_col(row):
        '''
        Calculate where filling should start for a given row.
        Pattern based on distance from seed:
        - dist 0: offset 0
        - dist 1: offset 2
        - dist 2-3: offset 6
        - dist 4-7: offset 14
        - dist 8-15: offset 30
        '''
        # Measure distance correctly for above and below
        if row < seed_row:
            dist = seed_row - row
        elif row > seed_row + 1:
            dist = row - (seed_row + 1)
        else:
            # Seed rows themselves
            return 0

        if dist == 0:
            return 0

        # Use bit_length to determine level
        # level = bit_length of distance
        level = dist.bit_length()

        # offset = sum of 2^i for i from 1 to level
        offset = 0
        for i in range(1, level + 1):
            offset += 2 ** i

        return offset

    def get_fractal_value(col, row, fill_start):
        '''
        Get the value for a cell based on the fractal pattern.
        The fractal pattern is continuous across the entire column space.
        Pattern: [seed], then alternating blocks of left/right values,
        with block size doubling every 2 blocks.
        - Cols 0-1: [left, right]  (seed row pattern)
        - Cols 2-3: [left, left]
        - Cols 4-5: [right, right]
        - Cols 6-9: [left, left, left, left]
        - Cols 10-13: [right, right, right, right]
        '''
        if col < fill_start:
            return 0

        # Determine which seed values to use based on row position
        is_top_half = row <= seed_row

        if is_top_half:
            left_val, right_val = tl, tr
        else:
            left_val, right_val = bl, br

        # Calculate fractal value based on absolute column position
        # The pattern is continuous, so we use col directly
        pos = col

        # Special case: seed columns
        if pos < 2:
            return left_val if pos == 0 else right_val

        # After seed, process blocks with doubling size
        pos -= 2
        block_size = 2
        block_index = 0

        while pos >= block_size:
            pos -= block_size
            block_index += 1
            # Double block size after every 2 blocks
            if block_index % 2 == 0:
                block_size *= 2

        # Return value based on block_index (alternating left-right)
        return left_val if block_index % 2 == 0 else right_val

    # Fill the grid
    for r in range(h):
        for c in range(w):
            if grid[r][c] != 0:
                # Keep seed values as is
                continue

            fill_start = get_fill_start_col(r)

            # Only fill if there's space (fill_start < width)
            if fill_start < w:
                result[r][c] = get_fractal_value(c, r, fill_start)

    return result


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("762cd429", solve)
