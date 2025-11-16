import os
from arc_tools.grid import Grid
from collections import deque
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Region coloring with walls and markers

    The grid contains:
    - Walls (1s): Form connected structures
    - Empty spaces (0s): Regions to be colored
    - Colored markers (2-9): Define colors for regions

    Rules:
    1. Markers adjacent to 1s color the entire connected 1-structure
    2. Markers with < 2 adjacent 1s flood-fill through connected 0s (not crossing 1s)
    3. Markers with >= 2 adjacent 1s only mark themselves (don't flood)

    This creates a Voronoi-like partition where markers spread their colors through
    empty regions, with walls acting as barriers.
    '''
    height = len(grid)
    width = len(grid[0])

    # Create output grid, copy input first
    output = [[grid[i][j] for j in range(width)] for i in range(height)]

    # Find all colored markers (non-0, non-1 values)
    markers = []
    for i in range(height):
        for j in range(width):
            if grid[i][j] not in [0, 1]:
                markers.append((i, j, grid[i][j]))

    # Find and color connected components of 1s
    visited_ones = set()

    def color_1s_component(start_i, start_j, color):
        """Color an entire connected component of 1s"""
        queue = deque([(start_i, start_j)])
        visited_ones.add((start_i, start_j))
        output[start_i][start_j] = color

        while queue:
            i, j = queue.popleft()
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < height and 0 <= nj < width:
                    if (ni, nj) not in visited_ones and grid[ni][nj] == 1:
                        visited_ones.add((ni, nj))
                        output[ni][nj] = color
                        queue.append((ni, nj))

    # For each marker, check if it's adjacent to any 1s
    for mi, mj, color in markers:
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = mi + di, mj + dj
            if 0 <= ni < height and 0 <= nj < width:
                if grid[ni][nj] == 1 and (ni, nj) not in visited_ones:
                    # This marker is adjacent to an uncolored 1-component
                    color_1s_component(ni, nj, color)

    # Now flood fill the 0-regions from each marker
    # But only if the marker has fewer than 2 adjacent 1s
    def flood_fill_zeros(start_i, start_j, color):
        """Flood fill through 0s only, not crossing 1s or markers"""
        queue = deque([(start_i, start_j)])
        visited = {(start_i, start_j)}

        while queue:
            i, j = queue.popleft()
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < height and 0 <= nj < width:
                    if (ni, nj) not in visited and grid[ni][nj] == 0:
                        visited.add((ni, nj))
                        output[ni][nj] = color
                        queue.append((ni, nj))

    def count_adjacent_ones(i, j):
        """Count how many 1s are adjacent to position (i, j)"""
        count = 0
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < height and 0 <= nj < width:
                if grid[ni][nj] == 1:
                    count += 1
        return count

    for mi, mj, color in markers:
        # Only flood fill if marker has fewer than 2 adjacent 1s
        if count_adjacent_ones(mi, mj) < 2:
            flood_fill_zeros(mi, mj, color)

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("477d2879", solve)
