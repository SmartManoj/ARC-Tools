import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from evaluation_tasks_v1.helper import solve_task


def solve(grid: Grid):
    '''
    Transform 4-connected components of 0s to 8s.

    Rules:
    - Find all connected components of 0s using 4-connectivity (horizontal/vertical only, no diagonals)
    - Isolated 0s (no 4-connected neighbors) stay as 0
    - 0s only connected diagonally (8-connected but not 4-connected) stay as 0
    - All 4-connected components (size > 1) become 8
    '''
    result = grid.copy()
    height, width = grid.height, grid.width
    visited = [[False] * width for _ in range(height)]

    def flood_fill(start_r, start_c):
        """
        Find all cells in the connected component of 0s starting from (start_r, start_c).
        Uses 4-connectivity (horizontal and vertical only, no diagonals).
        Returns: component_cells (list of (r, c) tuples)
        """
        if visited[start_r][start_c] or grid[start_r][start_c] != 0:
            return []

        component = []
        stack = [(start_r, start_c)]

        while stack:
            r, c = stack.pop()

            if r < 0 or r >= height or c < 0 or c >= width:
                continue
            if visited[r][c] or grid[r][c] != 0:
                continue

            visited[r][c] = True
            component.append((r, c))

            # Check only 4 cardinal neighbors (no diagonals)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < height and 0 <= nc < width:
                    if not visited[nr][nc] and grid[nr][nc] == 0:
                        stack.append((nr, nc))

        return component

    # Find all connected components of 0s
    for r in range(height):
        for c in range(width):
            if grid[r][c] == 0 and not visited[r][c]:
                component = flood_fill(r, c)

                # Convert to 8 if it's a 4-connected component with size > 1
                if len(component) > 1:
                    for cell_r, cell_c in component:
                        result[cell_r][cell_c] = 8

    return result


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("e0fb7511", solve)
