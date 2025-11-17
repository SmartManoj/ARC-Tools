import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Extract the largest connected component of non-zero values.
    '''
    h, w = grid.height, grid.width
    visited = [[False] * w for _ in range(h)]
    components = []

    def dfs(r, c, value):
        """Depth-first search to find connected component"""
        if r < 0 or r >= h or c < 0 or c >= w:
            return []
        if visited[r][c] or grid[r][c] != value:
            return []
        visited[r][c] = True
        cells = [(r, c)]
        # 4-connected neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            cells.extend(dfs(r + dr, c + dc, value))
        return cells

    # Find all connected components
    for r in range(h):
        for c in range(w):
            if not visited[r][c] and grid[r][c] != 0:
                component_cells = dfs(r, c, grid[r][c])
                if component_cells:
                    components.append((grid[r][c], component_cells))

    if not components:
        return grid

    # Find the largest component
    value, cells = max(components, key=lambda x: len(x[1]))

    # Extract bounding box
    min_r = min(r for r, c in cells)
    max_r = max(r for r, c in cells)
    min_c = min(c for r, c in cells)
    max_c = max(c for r, c in cells)

    out_h = max_r - min_r + 1
    out_w = max_c - min_c + 1

    # Create result grid
    result_data = [[0] * out_w for _ in range(out_h)]
    for r, c in cells:
        result_data[r - min_r][c - min_c] = grid[r][c]

    return Grid(result_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("73ccf9c2", solve)
