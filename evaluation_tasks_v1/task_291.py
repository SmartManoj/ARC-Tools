import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Find the 3x3 plus-shaped pattern that is enclosed within an orange (color 7) rectangular frame.
    The pattern consists of a 3x3 grid with the center cell as background color (gray/5) and
    surrounding cells forming a plus shape in another color.
    '''
    # Find all 3x3 plus-shaped patterns
    patterns = []
    for r in range(grid.height - 2):
        for c in range(grid.width - 2):
            # Check if this is a 3x3 plus pattern
            # Pattern: X X X
            #          X . X  (where . is center, X are all same non-background color)
            #          X X X
            center = grid[r+1, c+1]
            if center == Color.GRAY:  # Center should be gray (5)
                corners = [
                    grid[r, c], grid[r, c+2],
                    grid[r+2, c], grid[r+2, c+2]
                ]
                edges = [
                    grid[r, c+1], grid[r+1, c],
                    grid[r+1, c+2], grid[r+2, c+1]
                ]
                # All edges should be the same color and not gray
                if len(set(edges)) == 1 and edges[0] != Color.GRAY:
                    color = edges[0]
                    # Top and bottom middle should be this color
                    if all(e == color for e in edges):
                        patterns.append((r, c, color))

    # Find the orange (7) rectangular frame
    # Look for connected orange cells that form a frame
    orange_regions = []
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r, c] == Color.ORANGE:
                orange_regions.append((r, c))

    if not orange_regions:
        # If no frame, just return first pattern found
        if patterns:
            r, c, _ = patterns[0]
            return grid[r:r+3, c:c+3]

    # Find the bounding box of orange cells
    orange_rows = [r for r, c in orange_regions]
    orange_cols = [c for r, c in orange_regions]
    min_r, max_r = min(orange_rows), max(orange_rows)
    min_c, max_c = min(orange_cols), max(orange_cols)

    # Find which pattern is inside the orange frame
    for r, c, color in patterns:
        # Check if pattern center is within the orange bounding box
        pattern_center_r = r + 1
        pattern_center_c = c + 1
        if min_r < pattern_center_r < max_r and min_c < pattern_center_c < max_c:
            return grid[r:r+3, c:c+3]

    # Fallback: return first pattern
    if patterns:
        r, c, _ = patterns[0]
        return grid[r:r+3, c:c+3]

    return grid

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("bf699163", solve)
