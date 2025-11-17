import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Find all rectangular regions of non-background values.
    Extract each region as a separate grid.
    Composite all regions by overlaying them, keeping the first non-zero value at each position.
    '''
    h, w = grid.height, grid.width

    # Find background color (most common value)
    from collections import Counter
    all_vals = [grid[r][c] for r in range(h) for c in range(w)]
    counter = Counter(all_vals)
    bg_color = counter.most_common(1)[0][0]

    # Find all rectangular regions of non-background values
    visited = [[False] * w for _ in range(h)]
    regions = []

    def flood_fill(start_r, start_c):
        """Find all cells in connected component of non-background values"""
        stack = [(start_r, start_c)]
        cells = set()

        while stack:
            r, c = stack.pop()
            if r < 0 or r >= h or c < 0 or c >= w:
                continue
            if (r, c) in cells or visited[r][c]:
                continue
            if grid[r][c] == bg_color:
                continue

            cells.add((r, c))
            visited[r][c] = True

            # 4-connected neighbors
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                stack.append((r + dr, c + dc))

        return cells

    # Find all connected components
    for r in range(h):
        for c in range(w):
            if not visited[r][c] and grid[r][c] != bg_color:
                cells = flood_fill(r, c)
                if cells:
                    # Find bounding box
                    min_r = min(cell[0] for cell in cells)
                    max_r = max(cell[0] for cell in cells)
                    min_c = min(cell[1] for cell in cells)
                    max_c = max(cell[1] for cell in cells)

                    # Extract region as grid
                    region_h = max_r - min_r + 1
                    region_w = max_c - min_c + 1
                    region_grid = []

                    for ri in range(min_r, max_r + 1):
                        row = []
                        for ci in range(min_c, max_c + 1):
                            row.append(grid[ri][ci])
                        region_grid.append(row)

                    regions.append((min_r, region_grid))

    # Sort regions by their starting row
    regions.sort(key=lambda x: x[0])

    # Extract just the grids
    region_grids = [rg for _, rg in regions]

    if not region_grids:
        return grid

    # All regions should have the same dimensions
    region_h = len(region_grids[0])
    region_w = len(region_grids[0][0])

    # Composite regions: for each cell, keep the first non-zero value
    output = [[0] * region_w for _ in range(region_h)]

    for i in range(region_h):
        for j in range(region_w):
            for region in region_grids:
                if region[i][j] != 0:
                    output[i][j] = region[i][j]
                    break

    # Create result as Grid
    result = Grid(output)
    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("7c9b52a0", solve)
