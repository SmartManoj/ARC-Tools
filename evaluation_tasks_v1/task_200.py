import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Fill hollow rectangles based on their dimensions:
    - 3x3 rectangles: fill interior with color 5
    - 3x4 rectangles: fill interior with color 7
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find all connected regions of non-zero colors (rectangle borders)
    visited = [[False] * w for _ in range(h)]
    rectangles = []

    def flood_fill(start_r, start_c, color):
        """Find all cells of the same color connected to start position"""
        cells = []
        stack = [(start_r, start_c)]
        visited[start_r][start_c] = True

        while stack:
            r, c = stack.pop()
            cells.append((r, c))
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and result[nr][nc] == color:
                    visited[nr][nc] = True
                    stack.append((nr, nc))
        return cells

    # Find all connected regions of non-zero colors
    for r in range(h):
        for c in range(w):
            if not visited[r][c] and result[r][c] != 0:
                color = result[r][c]
                cells = flood_fill(r, c, color)

                # Get bounding box of the colored region
                min_r = min(cell[0] for cell in cells)
                max_r = max(cell[0] for cell in cells)
                min_c = min(cell[1] for cell in cells)
                max_c = max(cell[1] for cell in cells)

                height = max_r - min_r + 1
                width = max_c - min_c + 1

                rectangles.append({
                    'bounds': (min_r, max_r, min_c, max_c),
                    'size': (height, width)
                })

    # Fill interiors based on rectangle size
    for rect in rectangles:
        min_r, max_r, min_c, max_c = rect['bounds']
        height, width = rect['size']

        # Determine fill color based on size
        if height == 3 and width == 3:
            fill_color = 5
        else:
            fill_color = 7

        # Fill interior with appropriate color
        for r in range(min_r + 1, max_r):
            for c in range(min_c + 1, max_c):
                if result[r][c] == 0:
                    result[r][c] = fill_color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("84f2aca1", solve)
