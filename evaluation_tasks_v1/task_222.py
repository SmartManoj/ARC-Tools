import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Create concentric layers around a marker using a color pattern from row 0.
    Row 0 contains a pattern of colors, row 1 is a separator line.
    A marker (matching the first color) is placed somewhere in the grid.
    The output creates concentric boxes around the marker using the colors in reverse order.
    '''
    import numpy as np

    result = grid.copy()

    # Extract the pattern from row 0 (stop at first 0 or when pattern ends)
    pattern = []
    separator_color = None

    for col in range(grid.shape[1]):
        val = grid.data[0, col]
        if val == 0:
            break
        pattern.append(val)

    if len(pattern) == 0:
        return grid

    # Get the separator line color from row 1
    separator_color = grid.data[1, 0]

    # Check if there's a special marker in the pattern (after main pattern)
    # Sometimes the pattern ends with a special color that should be replaced
    # Look for the separator line color
    main_pattern = []
    for col, color in enumerate(pattern):
        if col < len(pattern) - 1 and pattern[col] != separator_color:
            main_pattern.append(color)
        elif color != separator_color:
            # This might be a special marker, check if we should replace it
            # For now, let's not include it in the main pattern
            pass

    # If pattern is not properly extracted, use all non-zero colors from row 0 before separator
    if len(main_pattern) == 0:
        main_pattern = []
        for col in range(grid.shape[1]):
            val = grid.data[0, col]
            if val == 0:
                break
            if val != separator_color:
                main_pattern.append(val)

    # Find the marker position (first color in pattern)
    marker_color = pattern[0] if pattern else None
    marker_pos = None

    for row in range(2, grid.shape[0]):  # Skip row 0 and 1
        for col in range(grid.shape[1]):
            if grid.data[row, col] == marker_color:
                marker_pos = (row, col)
                break
        if marker_pos:
            break

    if not marker_pos or not main_pattern:
        return grid

    # Create concentric layers around the marker
    marker_row, marker_col = marker_pos

    # Determine the size needed for the pattern
    # The outermost layer should be len(pattern) cells away from the marker
    radius = len(main_pattern)

    # Fill concentric layers
    for layer in range(radius):
        # Calculate which color to use (reverse order from outermost to innermost)
        color_idx = len(main_pattern) - 1 - layer
        color = main_pattern[color_idx]

        # Fill the current layer
        for dr in range(-radius + layer, radius - layer + 1):
            for dc in range(-radius + layer, radius - layer + 1):
                r, c = marker_row + dr, marker_col + dc

                # Check if we're on the border of this layer
                if abs(dr) == radius - layer - 1 or abs(dc) == radius - layer - 1:
                    if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                        result.data[r, c] = color

    # Keep the marker at the center
    result.data[marker_row, marker_col] = marker_color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("9356391f", solve)
