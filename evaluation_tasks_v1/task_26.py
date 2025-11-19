import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms the grid by identifying connected components of non-zero colors.
    - Connected components are defined using 4-connectivity (up, down, left, right)
    - If a connected component has fewer than 3 cells, all cells in that component are changed to color 3
    - Otherwise, cells retain their original color

    Pattern observed:
    - Small isolated cells or pairs of the same color (size < 3) -> color 3
    - Larger connected regions (size >= 3) -> keep original color
    '''
    height = grid.height
    width = grid.width

    # Create output grid as a copy of input
    output_data = [[grid[y][x] for x in range(width)] for y in range(height)]

    # Track visited cells
    visited = [[False] * width for _ in range(height)]

    def flood_fill(start_row, start_col, color):
        """Find all cells in a connected component using BFS"""
        if visited[start_row][start_col] or grid[start_row][start_col] == 0:
            return []

        component = []
        queue = [(start_row, start_col)]
        visited[start_row][start_col] = True

        while queue:
            r, c = queue.pop(0)
            component.append((r, c))

            # Check 4 neighbors (up, down, left, right)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < height and 0 <= nc < width and
                    not visited[nr][nc] and
                    grid[nr][nc] == color):
                    visited[nr][nc] = True
                    queue.append((nr, nc))

        return component

    # Find all connected components
    for r in range(height):
        for c in range(width):
            if not visited[r][c] and grid[r][c] != 0:
                color = grid[r][c]
                component = flood_fill(r, c, color)

                # If component size < 3, change all cells to color 3
                if len(component) < 3:
                    for cr, cc in component:
                        output_data[cr][cc] = 3

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("12eac192", solve)
