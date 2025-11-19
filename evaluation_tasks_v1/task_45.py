import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern analysis:
    1. Find the horizontal blue (1) line - the row with most blue cells
    2. Find continuous segments of blue in this line
    3. Find connected components of gray (5) cells below
    4. For each blue segment, change the first overlapping gray object to red (2)
       UNLESS the gray object extends beyond the right edge of the blue segment
    '''

    # Find blue structure
    blue_rows = []
    for r in range(len(grid)):
        if any(grid[r][c] == 1 for c in range(len(grid[0]))):
            blue_rows.append(r)

    if not blue_rows:
        return grid.copy()

    # Find horizontal blue line (row with most blue cells)
    horiz_line_row = max(blue_rows, key=lambda r: sum(1 for c in range(len(grid[0])) if grid[r][c] == 1))

    # Find continuous segments of blue (1) in the horizontal line
    blue_segments = []
    start = None
    for c in range(len(grid[0])):
        if grid[horiz_line_row][c] == 1:
            if start is None:
                start = c
        else:
            if start is not None:
                blue_segments.append((start, c - 1))
                start = None
    if start is not None:
        blue_segments.append((start, len(grid[0]) - 1))

    logger.info(f"Blue segments: {blue_segments}")

    # Find all gray (5) objects using flood fill
    visited = set()
    gray_objects = []

    def find_gray_object(r, c):
        """Flood fill to find connected gray cells"""
        if (r, c) in visited:
            return []
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
            return []
        if grid[r][c] != 5:
            return []

        visited.add((r, c))
        cells = [(r, c)]

        # 4-connected
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            cells.extend(find_gray_object(r + dr, c + dc))

        return cells

    # Find all gray objects
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 5 and (r, c) not in visited:
                obj_cells = find_gray_object(r, c)
                if obj_cells:
                    cols = [cell[1] for cell in obj_cells]
                    min_c, max_c = min(cols), max(cols)
                    gray_objects.append({
                        'min_col': min_c,
                        'max_col': max_c,
                        'cells': obj_cells
                    })

    # Sort gray objects by leftmost column
    gray_objects.sort(key=lambda obj: obj['min_col'])

    logger.info(f"Found {len(gray_objects)} gray objects")

    # For each blue segment, find the first overlapping gray object
    # and change it to red (2), unless it extends beyond the segment's right edge
    # AND the segment is the last (rightmost) segment
    output = grid.copy()
    grays_to_change = set()

    for seg_idx, (seg_start, seg_end) in enumerate(blue_segments):
        is_last_segment = (seg_idx == len(blue_segments) - 1)
        logger.info(f"Processing segment {seg_start}-{seg_end} (is_last: {is_last_segment})")

        # Find first gray object that overlaps with this segment
        for obj in gray_objects:
            obj_start = obj['min_col']
            obj_end = obj['max_col']

            # Check if object overlaps with segment
            if not (obj_end < seg_start or obj_start > seg_end):
                # Overlaps!
                logger.info(f"  Gray object at cols {obj_start}-{obj_end} overlaps")

                # Check if it extends beyond the right edge of the segment
                extends_right = obj_end > seg_end

                # Skip if extends right AND this is the last segment
                if extends_right and is_last_segment:
                    logger.info(f"    Extends beyond right edge ({obj_end} > {seg_end}) and is last segment, skipping")
                else:
                    # This is the first overlapping gray for this segment
                    logger.info(f"    Changing to red")
                    for cell in obj['cells']:
                        grays_to_change.add(cell)
                    break  # Only change the first one for this segment

    # Apply changes
    for r, c in grays_to_change:
        output[r][c] = 2

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("1acc24af", solve)
