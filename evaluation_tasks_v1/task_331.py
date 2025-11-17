import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    The grid contains 3x3 patterns at positions (1+4*i, 1+4*j).
    One pattern is colored with a special color (8) as a marker.
    Color the marker pattern with 8, and color other patterns with 7
    based on their frequency (patterns appearing frequently enough get colored).
    '''
    from collections import defaultdict

    result = grid.copy()

    # Function to extract a 3x3 pattern as a list of lists
    def extract_pattern(g, row_start, col_start):
        pattern = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(g[row_start + i][col_start + j])
            pattern.append(row)
        return pattern

    # Function to normalize pattern (convert all non-zero to 1)
    def normalize_pattern(pattern):
        normalized = []
        for row in pattern:
            norm_row = [1 if val > 0 else 0 for val in row]
            normalized.append(norm_row)
        return normalized

    # Function to convert pattern to hashable tuple
    def pattern_to_tuple(pattern):
        return tuple(tuple(row) for row in pattern)

    # Extract all 3x3 patterns and group by shape
    pattern_locations = []
    pattern_shapes = defaultdict(list)

    for row_start in range(1, grid.height - 2, 4):
        for col_start in range(1, grid.width - 2, 4):
            pattern = extract_pattern(grid, row_start, col_start)
            normalized = normalize_pattern(pattern)
            shape_key = pattern_to_tuple(normalized)

            pattern_locations.append((row_start, col_start, pattern))
            pattern_shapes[shape_key].append((row_start, col_start, pattern))

    # Find the marker pattern (one with color 8)
    marker_shape = None
    marker_pattern_colored = None
    for shape_key, locations in pattern_shapes.items():
        for row_start, col_start, pattern in locations:
            has_special_color = False
            for row in pattern:
                for val in row:
                    if val not in [0, 1]:
                        has_special_color = True
                        marker_shape = shape_key
                        marker_pattern_colored = pattern
                        break
                if has_special_color:
                    break
            if has_special_color:
                break
        if marker_shape:
            break

    # Calculate threshold for coloring (patterns must appear frequently enough)
    num_unique = len(pattern_shapes)
    counts = [len(locs) for locs in pattern_shapes.values()]
    counts.sort(reverse=True)

    # Use a threshold: color if count > num_unique / 2
    threshold = num_unique / 2

    # Color patterns
    for shape_key, locations in pattern_shapes.items():
        count = len(locations)

        # Determine color for this shape
        if shape_key == marker_shape:
            # This is the marker - use color 8
            color_pattern = marker_pattern_colored
        elif count > threshold:
            # Frequent enough - use color 7
            # Create a colored version of the pattern
            template = locations[0][2]
            color_pattern = []
            for row in template:
                colored_row = [7 if val > 0 else 0 for val in row]
                color_pattern.append(colored_row)
        else:
            # Not frequent enough - skip coloring
            continue

        # Apply the coloring
        for row_start, col_start, pattern in locations:
            for i in range(3):
                for j in range(3):
                    if color_pattern[i][j] > 0:
                        result[row_start + i][col_start + j] = color_pattern[i][j]

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("d94c3b52", solve)
