import os
from arc_tools.grid import Grid
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task


def solve(grid: Grid):
    '''
    Extract colored patterns from a grid and arrange them in a 7x7 output.

    Pattern:
    1. Find the 7x7 template box of 1s (contains color markers)
    2. Extract color markers from template positions:
       - Top-left: row 1, col 1
       - Top-right: row 1, col 5
       - Bottom-left: row 5, col 1
       - Bottom-right: row 5, col 5
    3. Find each colored pattern in the input (outside the template)
    4. Extract 3x3 bounding box for each pattern
    5. Arrange in 7x7 output:
       - Top-left quadrant (rows 0-2, cols 0-2): top-left color pattern
       - Top-right quadrant (rows 0-2, cols 4-6): top-right color pattern
       - Bottom-left quadrant (rows 4-6, cols 0-2): bottom-left color pattern
       - Bottom-right quadrant (rows 4-6, cols 4-6): bottom-right color pattern
       - Row 3 and column 3: separators (all 0s)
    '''
    h, w = grid.height, grid.width

    # Find the 7x7 template box of 1s
    ones_positions = []
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 1:
                ones_positions.append((r, c))

    if not ones_positions:
        return Grid([[0] * 7 for _ in range(7)])

    template_min_r = min(p[0] for p in ones_positions)
    template_max_r = max(p[0] for p in ones_positions)
    template_min_c = min(p[1] for p in ones_positions)
    template_max_c = max(p[1] for p in ones_positions)

    # Extract color markers from template
    colors_template = {}
    if template_max_r - template_min_r == 6 and template_max_c - template_min_c == 6:
        # Standard 7x7 template
        top_left_color = grid[template_min_r + 1][template_min_c + 1]
        top_right_color = grid[template_min_r + 1][template_min_c + 5]
        bottom_left_color = grid[template_min_r + 5][template_min_c + 1]
        bottom_right_color = grid[template_min_r + 5][template_min_c + 5]

        colors_template = {
            'top_left': top_left_color,
            'top_right': top_right_color,
            'bottom_left': bottom_left_color,
            'bottom_right': bottom_right_color,
        }

    # Helper function to find bounding box of a color (excluding template)
    def find_pattern_bbox(color):
        positions = []
        for r in range(h):
            for c in range(w):
                # Skip if in template
                if template_min_r <= r <= template_max_r and template_min_c <= c <= template_max_c:
                    continue
                if grid[r][c] == color:
                    positions.append((r, c))

        if not positions:
            return None, None, None, None

        min_r = min(p[0] for p in positions)
        max_r = max(p[0] for p in positions)
        min_c = min(p[1] for p in positions)
        max_c = max(p[1] for p in positions)

        return min_r, max_r, min_c, max_c

    # Helper function to extract a pattern and pad to 3x3
    def extract_pattern(color):
        min_r, max_r, min_c, max_c = find_pattern_bbox(color)
        if min_r is None:
            return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        # Extract the raw pattern first
        pattern = []
        for r in range(min_r, max_r + 1):
            row = []
            for c in range(min_c, max_c + 1):
                row.append(grid[r][c])
            pattern.append(row)

        height = len(pattern)
        width = len(pattern[0]) if pattern else 0

        # Expand to 3x3 if needed
        # If height < 3, prepend a reflection of the last row
        while height < 3:
            pattern.insert(0, pattern[-1])
            height += 1

        # If width < 3, prepend a reflection of the last column
        while width < 3:
            for row in pattern:
                row.insert(0, row[-1])
            width += 1

        # Take only first 3x3
        pattern = [row[:3] for row in pattern[:3]]

        return pattern

    # Extract patterns for each color
    patterns = {}
    for key, color in colors_template.items():
        if color != 1:  # Skip if it's actually a 1 (shouldn't happen)
            patterns[key] = extract_pattern(color)

    # Build 7x7 output
    result = [[0] * 7 for _ in range(7)]

    # Place patterns in quadrants
    # Top-left
    pattern = patterns.get('top_left', [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    for r in range(3):
        for c in range(3):
            result[r][c] = pattern[r][c]

    # Top-right
    pattern = patterns.get('top_right', [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    for r in range(3):
        for c in range(3):
            result[r][c + 4] = pattern[r][c]

    # Bottom-left
    pattern = patterns.get('bottom_left', [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    for r in range(3):
        for c in range(3):
            result[r + 4][c] = pattern[r][c]

    # Bottom-right
    pattern = patterns.get('bottom_right', [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    for r in range(3):
        for c in range(3):
            result[r + 4][c + 4] = pattern[r][c]

    # Row 3 and col 3 should be 0s (already are by default)

    return Grid(result)


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("7d18a6fb", solve)
