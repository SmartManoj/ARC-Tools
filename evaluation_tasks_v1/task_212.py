import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Reverses the colors of concentric rectangular layers.
    For each set of concentric rectangles, swaps the outermost color with the innermost,
    the second-outermost with the second-innermost, etc.
    '''
    result = grid.copy()
    h, w = len(grid), len(grid[0])
    visited = [[False] * w for _ in range(h)]

    for start_r in range(h):
        for start_c in range(w):
            if visited[start_r][start_c] or grid[start_r][start_c] == 0:
                continue

            # Find the bounding box of this connected region using flood fill
            region_cells = []
            stack = [(start_r, start_c)]
            temp_visited = set()

            while stack:
                r, c = stack.pop()
                if (r, c) in temp_visited or r < 0 or r >= h or c < 0 or c >= w:
                    continue
                if grid[r][c] == 0:
                    continue

                temp_visited.add((r, c))
                region_cells.append((r, c))

                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    stack.append((r + dr, c + dc))

            # Get bounding box
            rows = [r for r, c in region_cells]
            cols = [c for r, c in region_cells]
            min_r, max_r = min(rows), max(rows)
            min_c, max_c = min(cols), max(cols)

            # Group cells by color and find the layer order
            cells_by_color = {}
            for r, c in region_cells:
                visited[r][c] = True
                color = grid[r][c]
                if color not in cells_by_color:
                    cells_by_color[color] = []
                cells_by_color[color].append((r, c))

            # For each color, find its minimum distance from the bounding box edge
            # This determines the layer order (outermost to innermost)
            color_min_dist = {}
            for color, cells in cells_by_color.items():
                min_dist = float('inf')
                for r, c in cells:
                    dist = min(r - min_r, max_r - r, c - min_c, max_c - c)
                    min_dist = min(min_dist, dist)
                color_min_dist[color] = min_dist

            # Sort colors by their minimum distance (outermost first)
            sorted_colors = sorted(color_min_dist.keys(), key=lambda c: color_min_dist[c])
            reversed_colors = list(reversed(sorted_colors))

            # Create color mapping: old color -> new color
            color_map = {old: new for old, new in zip(sorted_colors, reversed_colors)}

            # Apply the color mapping
            for r, c in region_cells:
                old_color = grid[r][c]
                result[r][c] = color_map[old_color]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("8dae5dfc", solve)
