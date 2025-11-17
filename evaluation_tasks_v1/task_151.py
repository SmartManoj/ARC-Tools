import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find all connected regions of 0s that are enclosed by 5s.
    Fill the largest region with 8 and the smallest region with 7.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find all connected regions of 0s using flood fill
    visited = [[False] * w for _ in range(h)]
    regions = []

    def flood_fill(r, c):
        if r < 0 or r >= h or c < 0 or c >= w:
            return []
        if visited[r][c] or result[r][c] != 0:
            return []
        visited[r][c] = True
        cells = [(r, c)]
        # 4-connected neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            cells.extend(flood_fill(r + dr, c + dc))
        return cells

    # Find all regions of 0s
    for r in range(h):
        for c in range(w):
            if not visited[r][c] and result[r][c] == 0:
                region = flood_fill(r, c)
                if region:
                    regions.append(region)

    # Check if a region is enclosed by 5s (or grid boundaries)
    def is_region_enclosed(region):
        region_set = set(region)
        for r, c in region:
            # Check all 4 neighbors
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # If neighbor is within grid
                if 0 <= nr < h and 0 <= nc < w:
                    # If neighbor is not in region and not a 5, region is not enclosed
                    if (nr, nc) not in region_set and result[nr][nc] != 5:
                        return False
        return True

    # Filter to only enclosed regions
    enclosed_regions = [r for r in regions if is_region_enclosed(r)]

    if not enclosed_regions:
        return result

    # Find smallest and largest regions
    smallest_region = min(enclosed_regions, key=len)
    largest_region = max(enclosed_regions, key=len)

    # Fill smallest with 7
    for r, c in smallest_region:
        result[r][c] = 7

    # Fill largest with 8
    for r, c in largest_region:
        result[r][c] = 8

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("62ab2642", solve)
