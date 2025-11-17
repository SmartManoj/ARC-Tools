import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Extract hollow rectangles (rectangles with a border but empty interior)
    and arrange them in the output grid.

    Hollow rectangles are detected by finding rectangular objects where the
    interior contains 0s (black). The output arranges these rectangles either
    horizontally or vertically based on their relative positions in the input.
    '''
    objects = detect_objects(grid, ignore_colors=[0])

    # Find hollow rectangles
    hollow_rects = []
    for obj in objects:
        min_r, max_r = obj.region.y1, obj.region.y2
        min_c, max_c = obj.region.x1, obj.region.x2
        color = obj.color

        # Check if hollow (interior has 0s)
        is_hollow = False
        if max_r - min_r > 1 and max_c - min_c > 1:
            for r in range(min_r + 1, max_r):
                for c in range(min_c + 1, max_c):
                    if grid[r][c] == 0:
                        is_hollow = True
                        break
                if is_hollow:
                    break

        if is_hollow:
            hollow_rects.append({
                'color': color,
                'min_r': min_r,
                'max_r': max_r,
                'min_c': min_c,
                'max_c': max_c,
                'height': max_r - min_r + 1,
                'width': max_c - min_c + 1
            })

    if not hollow_rects:
        return grid

    # Determine arrangement direction based on spatial layout
    # Check if rectangles are more vertically or horizontally arranged
    avg_row = sum(r['min_r'] for r in hollow_rects) / len(hollow_rects)
    avg_col = sum(r['min_c'] for r in hollow_rects) / len(hollow_rects)

    row_variance = sum((r['min_r'] - avg_row) ** 2 for r in hollow_rects)
    col_variance = sum((r['min_c'] - avg_col) ** 2 for r in hollow_rects)

    # Sort by position
    if row_variance > col_variance:
        # Arranged vertically, stack vertically
        hollow_rects.sort(key=lambda r: r['min_r'])
        # Create output grid
        height = sum(r['height'] for r in hollow_rects)
        width = hollow_rects[0]['width']
        result = Grid([[0 for _ in range(width)] for _ in range(height)])

        current_r = 0
        for rect in hollow_rects:
            for r in range(rect['height']):
                for c in range(rect['width']):
                    val = grid[rect['min_r'] + r][rect['min_c'] + c]
                    result[current_r + r][c] = val
            current_r += rect['height']
    else:
        # Arranged horizontally, stack horizontally
        hollow_rects.sort(key=lambda r: r['min_c'])
        # Create output grid
        height = hollow_rects[0]['height']
        width = sum(r['width'] for r in hollow_rects)
        result = Grid([[0 for _ in range(width)] for _ in range(height)])

        current_c = 0
        for rect in hollow_rects:
            for r in range(rect['height']):
                for c in range(rect['width']):
                    val = grid[rect['min_r'] + r][rect['min_c'] + c]
                    result[r][current_c + c] = val
            current_c += rect['width']

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("a680ac02", solve)
