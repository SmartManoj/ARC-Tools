import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Copy a pattern to a target location using color 5 as markers

    1. Find all pixels with color 5 (markers)
    2. Identify source marker (has non-zero neighbors) vs target marker(s) (isolated)
    3. Copy all non-zero pixels around source marker to target location(s)
    4. The marker position itself (5) is not copied in the target
    '''
    # Find all color 5 markers
    markers = []
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r][c] == 5:
                markers.append((r, c))

    if len(markers) < 2:
        # No transformation needed
        return grid

    # Identify which marker is the source (has non-zero neighbors)
    source_marker = None
    target_markers = []

    for r, c in markers:
        # Count non-zero neighbors in a 5x5 area (excluding the marker itself)
        neighbors = 0
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                nr, nc = r + dr, c + dc
                if 0 <= nr < grid.height and 0 <= nc < grid.width:
                    val = grid[nr][nc]
                    if val != 0 and val != 5:
                        neighbors += 1

        if neighbors > 0:
            source_marker = (r, c)
        else:
            target_markers.append((r, c))

    # Create output grid starting with input
    output = grid.copy()

    # For each target marker, copy the pattern
    for target_r, target_c in target_markers:
        # Calculate offset
        src_r, src_c = source_marker
        offset_r = target_r - src_r
        offset_c = target_c - src_c

        # Copy all non-zero pixels from the entire grid, shifted by offset
        for r in range(grid.height):
            for c in range(grid.width):
                val = grid[r][c]
                # Copy all non-zero pixels except the marker itself
                if val != 0 and val != 5:
                    new_r = r + offset_r
                    new_c = c + offset_c
                    # Place in output if within bounds
                    if 0 <= new_r < grid.height and 0 <= new_c < grid.width:
                        output[new_r][new_c] = val

        # Remove the target marker (replace with 0)
        output[target_r][target_c] = 0

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("2c737e39", solve)
