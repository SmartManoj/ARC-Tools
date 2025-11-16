import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    ARC-AGI Task 08573cc6: Nested Rectangular Frames

    Creates nested rectangles around a marker, where:
    - Color1 (from [0,0]) is used for horizontal edges
    - Color2 (from [0,1]) is used for vertical edges and corners
    '''

    # Extract the two colors from top-left
    color_h = grid[0][0]  # Horizontal edges
    color_v = grid[0][1]  # Vertical edges and corners

    # Find the marker position (color 1)
    marker_row, marker_col = None, None
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 1:
                marker_row, marker_col = r, c
                break
        if marker_row is not None:
            break

    # Create output grid
    height = len(grid)
    width = len(grid[0])
    output = [[0] * width for _ in range(height)]

    # Calculate number of nested rectangles
    # Special case: if marker is on diagonal, always 2 layers
    if marker_row == marker_col:
        num_layers = 2
    else:
        num_layers = (min(marker_row, marker_col) + 1) // 2

    # Draw each layer from innermost to outermost
    for layer_idx in range(num_layers):
        if layer_idx == 0:
            # Innermost layer - starts at marker row
            top = marker_row
            left = marker_col - 2
            bottom = marker_row + 3
            right = marker_col + 2

            # Draw horizontal line at marker row (left to just before marker)
            for c in range(left, marker_col):
                if 0 <= c < width:
                    output[top][c] = color_h

            # Draw left vertical edge (below marker row)
            for r in range(top + 1, bottom + 1):
                if 0 <= r < height and 0 <= left < width:
                    output[r][left] = color_v

            # Draw bottom horizontal edge
            for c in range(left, right + 1):
                if 0 <= bottom < height and 0 <= c < width:
                    if c == left:
                        output[bottom][c] = color_v  # Corner
                    else:
                        output[bottom][c] = color_h

            # Draw right vertical edge (not including bottom corner)
            # For 3-layer case with marker_col > marker_row, start from layer 1's top
            if num_layers == 3 and marker_col > marker_row:
                right_start = marker_row - 2  # Layer 1's top
            else:
                right_start = top
            for r in range(right_start, bottom):
                if 0 <= r < height and 0 <= right < width:
                    output[r][right] = color_v

        elif layer_idx == 1:
            # Middle/Outer layer (depends on num_layers)
            top = marker_row - 2
            left = marker_col - 4

            # Right varies based on marker position
            if marker_col > marker_row:
                right = marker_col + 4
            else:
                right = marker_col + 2

            # Bottom varies based on configuration
            if num_layers == 2:
                # For diagonal markers, bottom extends further
                if marker_row == marker_col:
                    bottom = marker_row + 4
                else:
                    bottom = marker_row + 3
            else:
                bottom = marker_row + 5

            # Draw top horizontal edge
            # Top edge ends before the inner layer's right edge
            inner_right = marker_col + 2
            top_end = min(right, inner_right)
            for c in range(left, top_end):
                if 0 <= top < height and 0 <= c < width and output[top][c] == 0:
                    output[top][c] = color_h
            # Top-right corner only if we're at the full right edge
            if top_end == right and 0 <= top < height and 0 <= right < width and output[top][right] == 0:
                output[top][right] = color_v

            # Draw left vertical edge (start after top edge)
            start_row = marker_row + 1 if left == marker_col - 2 else top + 1
            for r in range(start_row, bottom + 1):
                if 0 <= r < height and 0 <= left < width and output[r][left] == 0:
                    output[r][left] = color_v

            # Draw right vertical edge (shares with inner if same column)
            # Start and end points vary based on configuration
            if num_layers == 2 and marker_row == marker_col:
                # Diagonal case: don't extend to bottom row
                right_start = top + 1
                right_end = bottom - 1
            elif num_layers == 3 and marker_col > marker_row:
                # Wide case: start from layer 2's top edge, extend to bottom
                right_start = marker_row - 4  # Layer 2's top
                right_end = bottom - 1  # Exclude bottom row
            elif num_layers == 3:
                # Tall case: stop at innermost layer's bottom
                right_start = top + 1
                right_end = marker_row + 3
            else:
                # Default
                right_start = top + 1
                right_end = bottom

            for r in range(right_start, right_end + 1):
                if 0 <= r < height and 0 <= right < width and output[r][right] == 0:
                    output[r][right] = color_v

            # Draw bottom horizontal edge (may be partial)
            if num_layers == 2:
                # Only bottom-left corner for 2-layer case
                if 0 <= bottom < height and 0 <= left < width and output[bottom][left] == 0:
                    output[bottom][left] = color_v
            else:
                # Full bottom edge for 3-layer case
                # Start from left + 1 to avoid the corner
                for c in range(left + 1, right + 1):
                    if 0 <= bottom < height and 0 <= c < width and output[bottom][c] == 0:
                        output[bottom][c] = color_h

        elif layer_idx == 2:
            # Outermost layer (only for 3-layer case)
            top = marker_row - 4

            # Bounds depend on whether marker_col > marker_row
            if marker_col > marker_row:
                # Wider configuration: left at col 0, extends to grid edges
                left = 0
                bottom = min(marker_row + (height - marker_row - 1), height - 1)
                right = min(marker_col + (width - marker_col - 1), width - 1)
            else:
                # Taller configuration: left at col 1, fixed offsets
                left = 1
                bottom = marker_row + 5
                right = marker_col + 4

            # Top edge always starts from col 0 for layer 2
            # Ends differently based on configuration
            if marker_col > marker_row:
                # Ends before layer 1's right edge
                layer1_right = marker_col + 4
                top_end = layer1_right - 1
            else:
                # Extends to right edge minus 1 (for the corner)
                top_end = right - 1

            for c in range(0, top_end + 1):
                if 0 <= top < height and 0 <= c < width and output[top][c] == 0:
                    output[top][c] = color_h
            # Draw top-right corner
            if 0 <= top < height and 0 <= right < width and output[top][right] == 0:
                output[top][right] = color_v

            # Left vertical edge starts from row marker_row + 1 or top + 1
            left_start = top + 1 if marker_col > marker_row else marker_row + 1
            for r in range(left_start, bottom + 1):
                if 0 <= r < height and 0 <= left < width and output[r][left] == 0:
                    output[r][left] = color_v

            # Right vertical edge
            # For marker_col > marker_row, start from row 0
            # Always exclude bottom row to let bottom edge handle the corner
            if marker_col > marker_row:
                right_start = 0
                right_end = bottom - 1  # Exclude bottom row
            else:
                right_start = top + 1
                right_end = bottom - 1  # Exclude bottom row

            for r in range(right_start, right_end + 1):
                if 0 <= r < height and 0 <= right < width and output[r][right] == 0:
                    output[r][right] = color_v

            # Bottom edge starts from col (left + 1)
            for c in range(left + 1, right + 1):
                if 0 <= bottom < height and 0 <= c < width and output[bottom][c] == 0:
                    output[bottom][c] = color_h

    # Place the marker back
    output[marker_row][marker_col] = 1

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("08573cc6", solve)
