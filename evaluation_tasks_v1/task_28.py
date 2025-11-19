import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    ARC task 13713586: Extend colored segments towards a boundary line (color 5).

    Pattern:
    1. Find a boundary line colored 5 (either a full row or full column)
    2. Find all colored segments (non-zero, non-5)
    3. Each segment extends perpendicular to the boundary towards it:
       - If boundary is horizontal: segments extend vertically
       - If boundary is vertical: segments extend horizontally
    4. When multiple segments could fill the same cell, the one furthest
       from the boundary (closest to its original position) takes priority
    '''

    height = grid.height
    width = grid.width

    # Find the boundary line (row or column of 5s)
    boundary_row = None
    boundary_col = None

    # Check for horizontal boundary (full row of 5s)
    for r in range(height):
        if all(grid[r][c] == 5 for c in range(width)):
            boundary_row = r
            break

    # Check for vertical boundary (full column of 5s)
    if boundary_row is None:
        for c in range(width):
            if all(grid[r][c] == 5 for r in range(height)):
                boundary_col = c
                break

    # Find all colored segments
    segments = []

    if boundary_row is not None:
        # Horizontal boundary - find horizontal segments
        for r in range(height):
            if r == boundary_row:
                continue
            for c in range(width):
                color = grid[r][c]
                if color != 0 and color != 5:
                    # Find the extent of this segment
                    start_col = c
                    end_col = c
                    while end_col + 1 < width and grid[r][end_col + 1] == color:
                        end_col += 1

                    segments.append({
                        'row': r,
                        'start_col': start_col,
                        'end_col': end_col,
                        'color': color
                    })

                    # Skip to end of segment
                    c = end_col

        # Create output grid
        output = [[0] * width for _ in range(height)]

        # Keep the boundary
        for c in range(width):
            output[boundary_row][c] = 5

        # Fill segments vertically towards boundary
        for segment in segments:
            seg_row = segment['row']
            start_col = segment['start_col']
            end_col = segment['end_col']
            color = segment['color']

            # Determine range to fill
            if seg_row < boundary_row:
                # Fill from seg_row down to boundary_row - 1
                for r in range(seg_row, boundary_row):
                    for c in range(start_col, end_col + 1):
                        # Check if this cell should be filled
                        # Prefer segments furthest from boundary (higher row number when boundary below)
                        current_color = output[r][c]
                        if current_color == 0:
                            output[r][c] = color
                        else:
                            # Check which segment is closer to its original position
                            # Find the segment that filled this cell
                            for other_seg in segments:
                                if (other_seg['color'] == current_color and
                                    other_seg['start_col'] <= c <= other_seg['end_col']):
                                    # Keep the one furthest from boundary
                                    if seg_row > other_seg['row']:
                                        output[r][c] = color
                                    break
            else:
                # Fill from seg_row up to boundary_row + 1
                for r in range(boundary_row + 1, seg_row + 1):
                    for c in range(start_col, end_col + 1):
                        current_color = output[r][c]
                        if current_color == 0:
                            output[r][c] = color
                        else:
                            # Check which segment is closer to its original position
                            for other_seg in segments:
                                if (other_seg['color'] == current_color and
                                    other_seg['start_col'] <= c <= other_seg['end_col']):
                                    # Keep the one furthest from boundary
                                    if seg_row < other_seg['row']:
                                        output[r][c] = color
                                    break

        return Grid(output)

    elif boundary_col is not None:
        # Vertical boundary - find vertical segments
        for c in range(width):
            if c == boundary_col:
                continue
            for r in range(height):
                color = grid[r][c]
                if color != 0 and color != 5:
                    # Find the extent of this segment
                    start_row = r
                    end_row = r
                    while end_row + 1 < height and grid[end_row + 1][c] == color:
                        end_row += 1

                    segments.append({
                        'col': c,
                        'start_row': start_row,
                        'end_row': end_row,
                        'color': color
                    })

                    # Skip to end of segment
                    r = end_row

        # Create output grid
        output = [[0] * width for _ in range(height)]

        # Keep the boundary
        for r in range(height):
            output[r][boundary_col] = 5

        # Fill segments horizontally towards boundary
        for segment in segments:
            seg_col = segment['col']
            start_row = segment['start_row']
            end_row = segment['end_row']
            color = segment['color']

            # Determine range to fill
            if seg_col < boundary_col:
                # Fill from seg_col right to boundary_col - 1
                for c in range(seg_col, boundary_col):
                    for r in range(start_row, end_row + 1):
                        current_color = output[r][c]
                        if current_color == 0:
                            output[r][c] = color
                        else:
                            # Check which segment is closer to its original position
                            for other_seg in segments:
                                if (other_seg['color'] == current_color and
                                    other_seg['start_row'] <= r <= other_seg['end_row']):
                                    # Keep the one furthest from boundary
                                    if seg_col > other_seg['col']:
                                        output[r][c] = color
                                    break
            else:
                # Fill from seg_col left to boundary_col + 1
                for c in range(boundary_col + 1, seg_col + 1):
                    for r in range(start_row, end_row + 1):
                        current_color = output[r][c]
                        if current_color == 0:
                            output[r][c] = color
                        else:
                            # Check which segment is closer to its original position
                            for other_seg in segments:
                                if (other_seg['color'] == current_color and
                                    other_seg['start_row'] <= r <= other_seg['end_row']):
                                    # Keep the one furthest from boundary
                                    if seg_col < other_seg['col']:
                                        output[r][c] = color
                                    break

        return Grid(output)

    # No boundary found, return original grid
    return grid

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("13713586", solve)
