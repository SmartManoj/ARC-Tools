import os
from collections import deque
from arc_tools.grid import Grid
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Move colored blocks down to compress them against an anchor row.
    Pattern: Find anchor row (fully filled), base pattern row (second-to-last),
    identify available columns (0s in base pattern), and place blocks there
    in a compressed format (smallest blocks first, filling available space).
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find anchor row (fully filled with single non-zero value)
    anchor_row = -1
    anchor_color = -1
    for r in range(h - 1, -1, -1):
        row_set = set(result[r])
        if len(row_set) == 1 and result[r][0] != 0:
            anchor_row = r
            anchor_color = result[r][0]
            break

    if anchor_row == -1 or anchor_row == 0:
        return result

    base_pattern_row = anchor_row - 1
    base_pattern = [result[base_pattern_row][c] for c in range(w)]

    # Find available columns (where base pattern has 0)
    available_cols = [c for c in range(w) if base_pattern[c] == 0]

    if not available_cols:
        return result

    # Find colored blocks (connected components above base pattern)
    visited = [[False] * w for _ in range(h)]
    blocks = []

    def flood_fill(start_r, start_c):
        """Find all cells of a connected component."""
        cells = []
        color = result[start_r][start_c]
        queue = deque([(start_r, start_c)])
        visited[start_r][start_c] = True

        while queue:
            r, c = queue.popleft()
            cells.append((r, c))

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < base_pattern_row and 0 <= nc < w and not visited[nr][nc]:
                    cell_color = result[nr][nc]
                    if cell_color == color:
                        visited[nr][nc] = True
                        queue.append((nr, nc))

        return cells, color

    # Find all blocks
    for r in range(base_pattern_row):
        for c in range(w):
            if not visited[r][c] and result[r][c] != 0 and result[r][c] != anchor_color:
                cells, color = flood_fill(r, c)
                blocks.append({
                    'color': color,
                    'cells': cells,
                    'min_r': min(r for r, c in cells),
                    'min_c': min(c for r, c in cells)
                })

    # Sort blocks by size (ascending), then by position
    blocks.sort(key=lambda b: (len(b['cells']), b['min_r'], b['min_c']))

    # Clear all cells above base pattern row
    for r in range(base_pattern_row):
        for c in range(w):
            result[r][c] = 0

    # Assign available columns to blocks and place them
    col_idx = 0
    for block in blocks:
        num_cells = len(block['cells'])
        color = block['color']

        # Blocks always have height 2, so columns needed = num_cells / 2
        num_assigned_cols = (num_cells + 1) // 2  # Ceiling division

        # Get the next available columns
        assigned_cols = available_cols[col_idx:col_idx + num_assigned_cols]
        col_idx += num_assigned_cols

        if not assigned_cols:
            break

        # Blocks always occupy exactly 2 rows: (base_pattern_row - 1) and base_pattern_row
        block_start_row = base_pattern_row - 1

        # Fill the assigned columns with the block color
        for row in range(block_start_row, base_pattern_row + 1):
            for col in assigned_cols:
                result[row][col] = color

    # Restore base pattern row (merge base pattern with placed blocks)
    for c in range(w):
        if base_pattern[c] != 0:  # Anchor pattern should be preserved
            result[base_pattern_row][c] = base_pattern[c]

    # Ensure anchor row is fully filled with anchor color
    for c in range(w):
        result[anchor_row][c] = anchor_color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("67c52801", solve)
