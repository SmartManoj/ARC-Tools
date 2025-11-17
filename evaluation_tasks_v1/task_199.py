import os
from arc_tools.grid import Grid
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Separate zeros into two groups based on edge-reachability using 4-connectivity:
    - Zeros reachable from grid edges (via 4-connectivity) -> become 2
    - Zeros not reachable from edges (enclosed) -> become 5
    - All 1s and 3s remain unchanged
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Flood fill from all grid edges using 4-connectivity only
    visited = [[False] * w for _ in range(h)]

    def flood_fill_4conn(start_r, start_c):
        """Flood fill from starting position using 4-connectivity (no diagonals)"""
        if start_r < 0 or start_r >= h or start_c < 0 or start_c >= w:
            return
        if visited[start_r][start_c] or result[start_r][start_c] != 0:
            return

        stack = [(start_r, start_c)]
        visited[start_r][start_c] = True

        while stack:
            r, c = stack.pop()
            # Check 4 neighbors (up, down, left, right - no diagonals)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and result[nr][nc] == 0:
                    visited[nr][nc] = True
                    stack.append((nr, nc))

    # Start flood fill from all zeros on the grid edges
    for r in range(h):
        for c in range(w):
            if (r == 0 or r == h - 1 or c == 0 or c == w - 1) and result[r][c] == 0 and not visited[r][c]:
                flood_fill_4conn(r, c)

    # Fill unreachable zeros with 5, edge-reachable zeros with 2
    for r in range(h):
        for c in range(w):
            if result[r][c] == 0:
                if visited[r][c]:
                    result[r][c] = 2
                else:
                    result[r][c] = 5

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("84db8fc4", solve)
