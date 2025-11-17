import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def find_colored_regions(grid: Grid):
    """Find all connected components of non-zero values."""
    h, w = grid.height, grid.width
    visited = [[False] * w for _ in range(h)]
    regions = {}  # color -> list of (row, col) coordinates

    def flood_fill(r, c, color, pixels):
        """DFS to find all connected pixels of same color."""
        if r < 0 or r >= h or c < 0 or c >= w:
            return
        if visited[r][c] or grid[r][c] != color:
            return
        visited[r][c] = True
        pixels.append((r, c))
        # 8-connected neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                flood_fill(r + dr, c + dc, color, pixels)

    # Find all regions
    for r in range(h):
        for c in range(w):
            if not visited[r][c] and grid[r][c] != 0:
                color = grid[r][c]
                pixels = []
                flood_fill(r, c, color, pixels)
                if color not in regions:
                    regions[color] = []
                regions[color].extend(pixels)

    return regions


def get_shape_info(pixels):
    """Get bounding box and extraction info for a set of pixels."""
    if not pixels:
        return None
    rows = [p[0] for p in pixels]
    cols = [p[1] for p in pixels]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    return {
        'min_r': min_r,
        'max_r': max_r,
        'min_c': min_c,
        'max_c': max_c,
        'height': max_r - min_r + 1,
        'width': max_c - min_c + 1
    }


def extract_pattern(grid: Grid, shape_info, color):
    """Extract the 3x3 pattern for a shape."""
    min_r, min_c = shape_info['min_r'], shape_info['min_c']
    max_r, max_c = shape_info['max_r'], shape_info['max_c']

    # Extract bounding box
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Create a 3x3 grid
    pattern = [[0] * 3 for _ in range(3)]

    # Fill in the pattern - map to 3x3
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r][c] == color:
                # Map to 3x3 coordinates
                if height == 1:
                    row_idx = 1  # center
                elif height == 2:
                    row_idx = 0 if (r - min_r) == 0 else 2
                else:
                    row_idx = min(2, int((r - min_r) * 3 / height))

                if width == 1:
                    col_idx = 1  # center
                elif width == 2:
                    col_idx = 0 if (c - min_c) == 0 else 2
                else:
                    col_idx = min(2, int((c - min_c) * 3 / width))

                pattern[row_idx][col_idx] = color

    return pattern


def solve(grid: Grid):
    """
    Extract colored shapes and arrange them in a grid.
    - Identify distinct colored regions
    - Extract 3x3 pattern for each color
    - Arrange horizontally or vertically based on overall bounding box
    """
    result = Grid([row[:] for row in grid])

    # Find all colored regions
    regions = find_colored_regions(result)

    if not regions:
        # No colored pixels, return empty grid
        return Grid([[0] * 3])

    # Get shape info for each color
    shape_info = {}
    for color, pixels in regions.items():
        info = get_shape_info(pixels)
        if info:
            shape_info[color] = info

    # Determine layout direction based on overall bounding box
    all_min_r = min(info['min_r'] for info in shape_info.values())
    all_max_r = max(info['max_r'] for info in shape_info.values())
    all_min_c = min(info['min_c'] for info in shape_info.values())
    all_max_c = max(info['max_c'] for info in shape_info.values())

    overall_height = all_max_r - all_min_r + 1
    overall_width = all_max_c - all_min_c + 1

    # Sort colors by position
    if overall_width > overall_height:
        # Horizontal arrangement: sort by leftmost column
        sorted_colors = sorted(shape_info.keys(), key=lambda c: shape_info[c]['min_c'])
        horizontal = True
    else:
        # Vertical arrangement: sort by topmost row
        sorted_colors = sorted(shape_info.keys(), key=lambda c: shape_info[c]['min_r'])
        horizontal = False

    # Extract patterns for each color
    patterns = []
    for color in sorted_colors:
        pattern = extract_pattern(result, shape_info[color], color)
        patterns.append(pattern)

    # Concatenate patterns
    if horizontal:
        # Concatenate horizontally: [3, num_colors*3]
        output = []
        for row_idx in range(3):
            row = []
            for pattern in patterns:
                row.extend(pattern[row_idx])
            output.append(row)
    else:
        # Concatenate vertically: [num_colors*3, 3]
        output = []
        for pattern in patterns:
            output.extend(pattern)

    return Grid(output)


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("67636eac", solve)
