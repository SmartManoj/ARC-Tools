import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task
from collections import Counter


def solve(grid: Grid):
    '''
    Pattern: Fill rectangular regions based on interior value frequency.

    1. Find all rectangular shapes outlined by a single color
    2. For each rectangle:
       - Count different non-zero values inside (excluding outline color)
       - If 2+ unique values exist: fill interior with most frequent value
       - Otherwise: clear interior to 0
    '''
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Create output as copy of input
    output = [[grid[r][c] for c in range(width)] for r in range(height)]

    # Track which cells are part of outlines or have been processed
    processed = set()

    # Find all unique colors (potential outline colors)
    colors = set()
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                colors.add(grid[r][c])

    # For each color, find all connected components
    for color in colors:
        # Find all cells with this color
        color_cells = set()
        for r in range(height):
            for c in range(width):
                if grid[r][c] == color:
                    color_cells.add((r, c))

        # Find all connected components for this color
        components = find_components(color_cells)

        # Mark cells in large components (4+ cells) as processed (preserved)
        for component in components:
            if len(component) >= 4:
                processed.update(component)

        # Try to find closed regions formed by this color
        regions = find_rectangles(color_cells, height, width)

        # For each region, check if we should fill it
        for outline, interior in regions:
            # Count interior values
            interior_values = []
            for r, c in interior:
                val = grid[r][c]
                if val != 0 and val != color:
                    interior_values.append(val)

            # Count unique values
            unique_values = set(interior_values)

            # Decide what to fill with
            if len(unique_values) >= 2:
                # Fill with most frequent value
                counts = Counter(interior_values)
                fill_value = counts.most_common(1)[0][0]
            else:
                # Clear to 0
                fill_value = 0

            # Fill the interior
            for r, c in interior:
                output[r][c] = fill_value
                processed.add((r, c))

    # Clear all unprocessed non-zero cells to 0 (isolated cells)
    for r in range(height):
        for c in range(width):
            if (r, c) not in processed and grid[r][c] != 0:
                output[r][c] = 0

    return Grid(output)


def find_components(cells):
    '''Find all connected components in the given set of cells.'''
    components = []
    visited = set()

    for cell in cells:
        if cell in visited:
            continue

        # BFS to find connected component
        component = set()
        queue = [cell]
        while queue:
            r, c = queue.pop(0)
            if (r, c) in visited:
                continue
            visited.add((r, c))
            component.add((r, c))

            # Check 4-connected neighbors
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in cells and (nr, nc) not in visited:
                    queue.append((nr, nc))

        components.append(component)

    return components


def find_rectangles(cells, height, width):
    '''Find all closed regions formed by the given cells.'''
    regions = []

    # Group cells by connected components
    components = find_components(cells)

    for component in components:
        # Skip if component is too small
        if len(component) < 4:
            continue

        # Find bounding box
        min_r = min(r for r, c in component)
        max_r = max(r for r, c in component)
        min_c = min(c for r, c in component)
        max_c = max(c for r, c in component)

        # Find interior cells using scanline approach
        interior = find_interior(component, min_r, max_r, min_c, max_c, height, width)

        if len(interior) > 0:
            regions.append((component, interior))

    return regions


def find_interior(outline, min_r, max_r, min_c, max_c, height, width):
    '''Find cells that are inside the outlined region using scanline approach.'''
    interior = set()

    # For each row, find cells between leftmost and rightmost outline cells
    for r in range(min_r, max_r + 1):
        # Find outline cells in this row
        outline_cols = sorted([c for row, c in outline if row == r])

        if len(outline_cols) >= 2:
            # Cells between min and max outline columns are potentially interior
            for c in range(outline_cols[0] + 1, outline_cols[-1]):
                if (r, c) not in outline:
                    interior.add((r, c))

    return interior


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("4b6b68e5", solve)
