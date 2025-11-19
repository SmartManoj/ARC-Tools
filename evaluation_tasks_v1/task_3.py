import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Finds rectangles bounded by 2s and fills their interiors based on size:
    - Interior 3×3 → fill with 8
    - Interior 5×5 → fill with 4
    - Interior 7×7 → fill with 3

    The algorithm detects rectangular regions where the border is made of 2s,
    calculates the interior dimensions (excluding borders), and fills all 0s
    inside with the appropriate color while preserving any existing 2s.
    '''
    # Create a copy of the input data
    output_data = [[grid[r][c] for c in range(grid.width)] for r in range(grid.height)]
    height = grid.height
    width = grid.width

    # Track which cells belong to processed rectangles
    processed = [[False] * width for _ in range(height)]

    # Find all rectangles by scanning for potential top-left corners
    for r in range(height):
        for c in range(width):
            # Look for a 2 that could be a top-left corner
            if output_data[r][c] == 2 and not processed[r][c]:
                # Try to find the extent of a rectangle starting here
                # Find width: how far right do the 2s extend in the top row?
                rect_width = 0
                for c2 in range(c, width):
                    if output_data[r][c2] == 2:
                        rect_width += 1
                    else:
                        break

                if rect_width < 3:  # Need at least 3 cells for a rectangle with interior
                    continue

                # Find height: how far down do the 2s extend in the left column?
                rect_height = 0
                for r2 in range(r, height):
                    if output_data[r2][c] == 2:
                        rect_height += 1
                    else:
                        break

                if rect_height < 3:  # Need at least 3 cells for a rectangle with interior
                    continue

                # Verify this forms a complete rectangle by checking all four edges
                is_valid_rect = True

                # Check if bottom-right corner is within bounds
                if r + rect_height > height or c + rect_width > width:
                    continue

                # Check top edge (all 2s)
                for c2 in range(c, c + rect_width):
                    if output_data[r][c2] != 2:
                        is_valid_rect = False
                        break

                # Check bottom edge (all 2s)
                if is_valid_rect:
                    for c2 in range(c, c + rect_width):
                        if output_data[r + rect_height - 1][c2] != 2:
                            is_valid_rect = False
                            break

                # Check left edge (all 2s)
                if is_valid_rect:
                    for r2 in range(r, r + rect_height):
                        if output_data[r2][c] != 2:
                            is_valid_rect = False
                            break

                # Check right edge (all 2s)
                if is_valid_rect:
                    for r2 in range(r, r + rect_height):
                        if output_data[r2][c + rect_width - 1] != 2:
                            is_valid_rect = False
                            break

                if is_valid_rect:
                    # Calculate interior dimensions (excluding the border)
                    interior_width = rect_width - 2
                    interior_height = rect_height - 2

                    # Determine fill color based on interior dimensions
                    fill_color = None
                    if interior_width == 3 and interior_height == 3:
                        fill_color = 8
                    elif interior_width == 5 and interior_height == 5:
                        fill_color = 4
                    elif interior_width == 7 and interior_height == 7:
                        fill_color = 3

                    if fill_color is not None:
                        # Fill the interior, only replacing 0s (preserve any 2s inside)
                        for r2 in range(r + 1, r + rect_height - 1):
                            for c2 in range(c + 1, c + rect_width - 1):
                                if output_data[r2][c2] == 0:
                                    output_data[r2][c2] = fill_color

                        # Mark this rectangle as processed
                        for r2 in range(r, r + rect_height):
                            for c2 in range(c, c + rect_width):
                                processed[r2][c2] = True

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("00dbd492", solve)
