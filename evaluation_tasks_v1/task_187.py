import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Extract a rectangular region from the input grid based on specific criteria:
    1. Find all rectangular regions of connected non-zero values (1s, 4s, 6s)
    2. Select the region with the minimum number of 4s and 6s (markers)
    3. If tied, prefer width 5, then width 6
    4. Extract and return that rectangular region
    '''
    h, w = grid.height, grid.width

    # Find all rectangular regions of connected non-zero values
    visited = [[False] * w for _ in range(h)]
    rectangles = []

    def flood_fill(start_r, start_c):
        """Find all connected non-zero cells"""
        if visited[start_r][start_c] or grid[start_r][start_c] == 0:
            return []

        queue = [(start_r, start_c)]
        cells = []
        visited[start_r][start_c] = True

        while queue:
            r, c = queue.pop(0)
            cells.append((r, c))

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w:
                    if not visited[nr][nc] and grid[nr][nc] != 0:
                        visited[nr][nc] = True
                        queue.append((nr, nc))

        return cells

    # Find all regions
    for r in range(h):
        for c in range(w):
            if not visited[r][c] and grid[r][c] != 0:
                cells = flood_fill(r, c)
                if cells:
                    min_r = min(rr for rr, cc in cells)
                    max_r = max(rr for rr, cc in cells)
                    min_c = min(cc for rr, cc in cells)
                    max_c = max(cc for rr, cc in cells)

                    width = max_c - min_c + 1
                    height = max_r - min_r + 1

                    # Count markers (4s and 6s)
                    count_4 = sum(1 for rr, cc in cells if grid[rr][cc] == 4)
                    count_6 = sum(1 for rr, cc in cells if grid[rr][cc] == 6)
                    total_markers = count_4 + count_6

                    rectangles.append({
                        'bounds': (min_r, max_r, min_c, max_c),
                        'width': width,
                        'height': height,
                        'markers': total_markers
                    })

    # Select the best rectangle based on criteria
    if not rectangles:
        return Grid([row[:] for row in grid])

    # Primary criterion: minimum marker count
    min_markers = min(r['markers'] for r in rectangles)
    candidates = [r for r in rectangles if r['markers'] == min_markers]

    # Tiebreaker: prefer width 5, then width 6
    width_5 = [r for r in candidates if r['width'] == 5]
    if width_5:
        selected = width_5[0]
    else:
        width_6 = [r for r in candidates if r['width'] == 6]
        if width_6:
            selected = width_6[0]
        else:
            selected = candidates[0]

    # Extract the selected rectangle
    min_r, max_r, min_c, max_c = selected['bounds']
    result = Grid([grid[r][min_c:max_c+1] for r in range(min_r, max_r+1)])

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("7bb29440", solve)
