import os
from arc_tools.grid import Grid
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find the reference block marked by 6s.
    Conversion rule:
    - Keep the reference block unchanged
    - Convert 8s to 4s based on proximity to reference:
      If column distance <= 2 from reference: keep 8s
      If column distance >= 3 from reference: convert 8s to 4s
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find the reference position (first 6)
    ref_r = None
    ref_c = None
    for r in range(h):
        for c in range(w):
            if result[r][c] == 6:
                ref_r = r
                ref_c = c
                break
        if ref_r is not None:
            break

    if ref_r is None:
        return result

    # Find all horizontal and vertical dividers (rows/columns of all 0s)
    h_dividers = []
    for r in range(h):
        if all(result[r][c] == 0 for c in range(w)):
            h_dividers.append(r)

    v_dividers = []
    for c in range(w):
        if all(result[r][c] == 0 for r in range(h)):
            v_dividers.append(c)

    # Find the reference block boundaries and block id
    ref_h_start = ref_h_end = ref_v_start = ref_v_end = None
    ref_block_i = ref_block_j = None
    for i in range(len(h_dividers) - 1):
        h_start = h_dividers[i] + 1
        h_end = h_dividers[i + 1]
        if h_start <= ref_r < h_end:
            ref_h_start, ref_h_end = h_start, h_end
            ref_block_i = i
            break

    for j in range(len(v_dividers) - 1):
        v_start = v_dividers[j] + 1
        v_end = v_dividers[j + 1]
        if v_start <= ref_c < v_end:
            ref_v_start, ref_v_end = v_start, v_end
            ref_block_j = j
            break

    # Convert 8s to 4s based on distance from reference
    for r in range(h):
        for c in range(w):
            if result[r][c] != 8:
                continue

            # Check if in reference block
            if (ref_h_start <= r < ref_h_end and
                ref_v_start <= c < ref_v_end):
                continue

            # Calculate distance from reference
            col_dist = abs(c - ref_c)
            row_dist = abs(r - ref_r)

            # Decision logic:
            # If only one v-block (len == 2), use column distance
            # If only one h-block (len == 2), use similar logic but for h-blocks
            # Otherwise use block-based logic

            if len(v_dividers) == 2:  # Single v-block, multiple h-blocks
                # Use column distance
                if col_dist <= 2:
                    continue  # Preserve
                else:
                    result[r][c] = 4  # Convert
            elif len(h_dividers) == 2:  # Single h-block, multiple v-blocks
                # Use column distance for this case too (columns act like blocks)
                if col_dist <= 2:
                    continue  # Preserve
                else:
                    result[r][c] = 4  # Convert
            else:
                # Multiple blocks in both dimensions
                # Find which block this cell is in
                in_ref_block = False
                for i in range(len(h_dividers) - 1):
                    h_start = h_dividers[i] + 1
                    h_end = h_dividers[i + 1]
                    if h_start <= r < h_end:
                        for j in range(len(v_dividers) - 1):
                            v_start = v_dividers[j] + 1
                            v_end = v_dividers[j + 1]
                            if v_start <= c < v_end:
                                # Found the block
                                # Convert unless it's the reference block
                                if (i, j) != (ref_block_i, ref_block_j):
                                    result[r][c] = 4
                                break
                        break

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("7d419a02", solve)
