import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find two 2s marking a rectangular region. Within this region, replace
    0s with 4s, using flood fill from the center of the bounding box to
    identify connected regions that should be filled.
    '''
    # Find the two 2s
    twos = []
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] == 2:
                twos.append((r, c))

    if len(twos) != 2:
        return grid

    (r1, c1), (r2, c2) = twos
    min_row, max_row = min(r1, r2), max(r1, r2)
    min_col, max_col = min(c1, c2), max(c1, c2)

    output = grid.copy()

    # Flood fill from center of bbox
    mid_r = (min_row + max_row) // 2
    mid_c = (min_col + max_col) // 2

    # Find starting point - prefer center, but use any 0 in bbox
    start_r, start_c = mid_r, mid_c
    if output[mid_r][mid_c] != 0:
        # Find first 0 in bbox
        found = False
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                if output[r][c] == 0:
                    start_r, start_c = r, c
                    found = True
                    break
            if found:
                break

        if not found:
            return output

    # Flood fill
    visited = set()
    queue = [(start_r, start_c)]

    while queue:
        r, c = queue.pop(0)
        if (r, c) in visited:
            continue
        if r < min_row or r > max_row or c < min_col or c > max_col:
            continue
        if output[r][c] != 0:
            continue

        visited.add((r, c))
        output[r][c] = 4

        # Add neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in visited and min_row <= nr <= max_row and min_col <= nc <= max_col:
                queue.append((nr, nc))

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("b15fca0b", solve)
