import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task
from collections import deque

def solve(grid: Grid):
    '''
    Pattern: Fill rectangular regions with marker colors

    The grid contains:
    - 0s (background)
    - 1s (borders/structure)
    - Marker values (2, 3, 4, 6, 8, etc.) indicating fill colors

    Algorithm:
    1. Find connected components of non-0 cells
    2. For each component with a marker, use iterative spreading:
       - Start from the marker
       - Spread to adjacent 1s that are completely surrounded (4 non-0 neighbors)
       - Continue spreading until no more cells can be filled
    '''
    height = grid.height
    width = grid.width

    # Create a copy of the grid data
    output_data = [row[:] for row in list(grid)]

    # Track visited cells for component finding
    visited = [[False] * width for _ in range(height)]

    def count_nonzero_neighbors(r, c):
        """Count how many non-0 neighbors a cell has."""
        count = 0
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and grid[nr][nc] != 0:
                count += 1
        return count

    def flood_fill(start_r, start_c):
        """Find a connected region of non-0 cells and any marker value."""
        region = []
        marker = None
        queue = deque([(start_r, start_c)])
        visited[start_r][start_c] = True

        while queue:
            r, c = queue.popleft()
            region.append((r, c))
            cell_value = grid[r][c]

            if cell_value > 1:
                marker = cell_value

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < height and 0 <= nc < width and
                    not visited[nr][nc] and grid[nr][nc] != 0):
                    visited[nr][nc] = True
                    queue.append((nr, nc))

        return region, marker

    def find_rectangles_and_fill(region, marker):
        """Find all rectangular sub-regions and fill their interiors."""
        region_set = set(region)

        # For each cell in the region, try to find rectangles starting from it
        for r, c in region:
            if output_data[r][c] != 1:  # Only look for rectangles of 1s
                continue

            # Try different rectangle sizes
            for height_r in range(3, 20):  # min size 3x3
                for width_r in range(3, 20):
                    # Check if this forms a valid rectangle of non-0s
                    is_rect = True
                    for rr in range(r, r + height_r):
                        for cc in range(c, c + width_r):
                            if rr >= height or cc >= width or (rr, cc) not in region_set or grid[rr][cc] == 0:
                                is_rect = False
                                break
                        if not is_rect:
                            break

                    if is_rect:
                        # Fill the interior (exclude border)
                        for rr in range(r + 1, r + height_r - 1):
                            for cc in range(c + 1, c + width_r - 1):
                                if output_data[rr][cc] == 1:
                                    output_data[rr][cc] = marker

    # Find all regions and fill them
    for r in range(height):
        for c in range(width):
            if not visited[r][c] and grid[r][c] != 0:
                region, marker = flood_fill(r, c)

                if marker is not None:
                    find_rectangles_and_fill(region, marker)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("09c534e7", solve)
