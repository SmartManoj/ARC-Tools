import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Draw vertical dividers at marker positions and fill columns with 2s
    to divide regions. Markers are columns with value 2 in the last row.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find marker row and columns
    marker_row_idx = -1
    for i in range(h):
        if 2 in grid[i]:
            marker_row_idx = i
            break

    if marker_row_idx == -1:
        return result

    marker_cols = [c for c in range(w) if grid[marker_row_idx][c] == 2]

    if not marker_cols:
        return result

    # Helper function to find consecutive blocks of 0s in a column
    def find_zero_blocks(col_idx):
        """Return list of (start_row, end_row) tuples for consecutive 0 blocks"""
        blocks = []
        in_block = False
        block_start = None

        for r in range(marker_row_idx):  # Don't include marker row itself
            val = grid[r][col_idx]
            if val == 0:
                if not in_block:
                    in_block = True
                    block_start = r
            else:
                if in_block:
                    in_block = False
                    blocks.append((block_start, r - 1))

        if in_block:
            blocks.append((block_start, marker_row_idx - 1))

        return blocks

    # Fill marker columns
    for i, marker_col in enumerate(marker_cols):
        blocks = find_zero_blocks(marker_col)

        if not blocks:
            continue

        # Determine which block to fill
        if i == len(marker_cols) - 1:
            # Last marker: fill the first block
            block = blocks[0]
        else:
            # Non-last marker: fill the last block
            block = blocks[-1]

        # Fill the block
        for r in range(block[0], block[1] + 1):
            if result[r][marker_col] == 0:
                result[r][marker_col] = 2

    # Process right neighbors and extensions
    for i, marker_col in enumerate(marker_cols):
        # Try to fill columns to the right
        next_marker = marker_cols[i+1] if i+1 < len(marker_cols) else w

        # Fill right neighbor
        right_col = marker_col + 1
        if right_col >= w:
            continue

        blocks = find_zero_blocks(right_col)

        if not blocks:
            # Also check if marker row itself is 0
            if grid[marker_row_idx][right_col] == 0:
                result[marker_row_idx][right_col] = 2
            continue

        # Determine which block to fill for right neighbors
        if i == len(marker_cols) - 1:
            # Right neighbor of last marker
            marker_blocks = find_zero_blocks(marker_col)
            if marker_blocks:
                first_marker_block_start = marker_blocks[0][0]
                # Fill blocks in right neighbor that come before the marker fills
                filled_any = False
                for block in blocks:
                    if block[1] < first_marker_block_start:
                        for r in range(block[0], block[1] + 1):
                            if result[r][right_col] == 0:
                                result[r][right_col] = 2
                                filled_any = True
                    elif block[0] < first_marker_block_start:
                        for r in range(block[0], first_marker_block_start + 1):
                            if result[r][right_col] == 0:
                                result[r][right_col] = 2
                                filled_any = True
                        break

                # If no blocks before marker, fill the marker row itself if it's 0
                if not filled_any and grid[marker_row_idx][right_col] == 0:
                    result[marker_row_idx][right_col] = 2
            else:
                # No marker block, so fill the last block entirely
                block = blocks[-1]
                for r in range(block[0], block[1] + 1):
                    if result[r][right_col] == 0:
                        result[r][right_col] = 2
        else:
            # Right neighbor of non-last marker: fill the last block
            block = blocks[-1]
            end_row = min(block[1], marker_row_idx - 2)
            for r in range(block[0], end_row + 1):
                if result[r][right_col] == 0:
                    result[r][right_col] = 2

        # Handle intermediate columns between markers
        # For very close markers (distance <= 3), fill intermediate columns
        gap_size = next_marker - marker_col
        if gap_size <= 3 and i < len(marker_cols) - 1:
            # Fill columns between this marker and next
            for col in range(right_col + 1, next_marker):
                col_blocks = find_zero_blocks(col)
                if col_blocks:
                    # Fill the last block
                    block = col_blocks[-1]
                    end_row = min(block[1], marker_row_idx - 2)
                    for r in range(block[0], end_row + 1):
                        if result[r][col] == 0:
                            result[r][col] = 2

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("712bf12e", solve)
