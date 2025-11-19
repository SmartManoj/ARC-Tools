import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task
from collections import deque

def solve(grid: Grid):
    '''
    Pattern: Find rectangular regions outlined by 1s (with gaps/openings)
    1. Identify connected components of 1s forming hollow rectangles
    2. Fill interior cells (non-1 cells within bounding box) with 2s
    3. Find gaps in the rectangle borders (missing 1s on the perimeter)
    4. Extend 2s from gaps outward to the edge of the grid
    '''
    output_data = [[grid[y][x] for x in range(grid.width)] for y in range(grid.height)]

    # Find connected components of 1s
    visited = set()
    components = []

    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] == 1 and (r, c) not in visited:
                # BFS to find connected component
                component = set()
                queue = deque([(r, c)])
                while queue:
                    cr, cc = queue.popleft()
                    if (cr, cc) in visited:
                        continue
                    if grid[cr][cc] != 1:
                        continue
                    visited.add((cr, cc))
                    component.add((cr, cc))

                    # Check 4 neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < grid.height and 0 <= nc < grid.width:
                            if (nr, nc) not in visited:
                                queue.append((nr, nc))

                if component:
                    components.append(component)

    # Process each component
    for component in components:
        # Find bounding box
        min_r = min(r for r, c in component)
        max_r = max(r for r, c in component)
        min_c = min(c for r, c in component)
        max_c = max(c for r, c in component)

        # Fill interior cells with 2
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if (r, c) not in component:
                    output_data[r][c] = 2

        # Find gaps in borders and extend
        # Top border
        for c in range(min_c, max_c + 1):
            if (min_r, c) not in component:
                # Extend upward
                for r in range(min_r - 1, -1, -1):
                    output_data[r][c] = 2

        # Bottom border
        for c in range(min_c, max_c + 1):
            if (max_r, c) not in component:
                # Extend downward
                for r in range(max_r + 1, grid.height):
                    output_data[r][c] = 2

        # Left border
        for r in range(min_r, max_r + 1):
            if (r, min_c) not in component:
                # Extend leftward
                for c in range(min_c - 1, -1, -1):
                    output_data[r][c] = 2

        # Right border
        for r in range(min_r, max_r + 1):
            if (r, max_c) not in component:
                # Extend rightward
                for c in range(max_c + 1, grid.width):
                    output_data[r][c] = 2

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("292dd178", solve)
