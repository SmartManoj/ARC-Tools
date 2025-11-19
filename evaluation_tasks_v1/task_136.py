import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern identified:
    1. Input has regions separated by 0s: two pattern regions + one canvas
    2. One pattern has base color 2 (this is the key pattern to use)
    3. Extract positions where 8s appear in the pattern with base color 2
    4. Tile this pattern strategically across the canvas:
       - For even vertical tiles: Place pattern in CENTER horizontal position
       - For odd vertical tiles: Place pattern on LEFT and RIGHT edges
    '''

    height, width = len(grid), len(grid[0])

    # Find all rectangular regions separated by 0s
    regions = []
    visited = [[False] * width for _ in range(height)]

    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0 and not visited[r][c]:
                queue = [(r, c)]
                visited[r][c] = True
                cells = [(r, c)]

                # BFS to find all connected non-zero cells
                while queue:
                    cr, cc = queue.pop(0)
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < height and 0 <= nc < width and not visited[nr][nc] and grid[nr][nc] != 0:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                            cells.append((nr, nc))

                if cells:
                    rows = [cell[0] for cell in cells]
                    cols = [cell[1] for cell in cells]
                    min_r, max_r = min(rows), max(rows)
                    min_c, max_c = min(cols), max(cols)

                    # Extract the region content
                    region_height = max_r - min_r + 1
                    region_width = max_c - min_c + 1
                    region_data = []
                    for rr in range(min_r, max_r + 1):
                        row = []
                        for cc in range(min_c, max_c + 1):
                            row.append(grid[rr][cc])
                        region_data.append(row)

                    # Count unique colors in region
                    colors = set()
                    for row in region_data:
                        for cell in row:
                            if cell != 0:
                                colors.add(cell)

                    regions.append({
                        'data': region_data,
                        'height': region_height,
                        'width': region_width,
                        'colors': colors,
                        'area': region_height * region_width
                    })

    # Find the canvas (largest region with uniform color - no 8s, no 2s)
    canvas = None
    pattern_2 = None  # Pattern with base color 2

    for region in sorted(regions, key=lambda x: x['area'], reverse=True):
        if len(region['colors']) == 1 and 8 not in region['colors'] and 2 not in region['colors']:
            canvas = region
            break

    # Find pattern with base color 2
    for region in regions:
        if region != canvas and 2 in region['colors'] and 8 in region['colors']:
            # Extract pattern as binary (1 where 8, 0 elsewhere)
            pattern = []
            for row in region['data']:
                pattern_row = [1 if cell == 8 else 0 for cell in row]
                pattern.append(pattern_row)

            pattern_2 = {
                'pattern': pattern,
                'height': region['height'],
                'width': region['width']
            }
            break

    if canvas is None or pattern_2 is None:
        return grid

    canvas_color = list(canvas['colors'])[0]
    canvas_height = canvas['height']
    canvas_width = canvas['width']

    # Create output grid filled with canvas color
    output = [[canvas_color] * canvas_width for _ in range(canvas_height)]

    # Calculate tiling dimensions
    pattern = pattern_2['pattern']
    p_height = pattern_2['height']
    p_width = pattern_2['width']

    num_vertical_tiles = canvas_height // p_height
    num_horizontal_tiles = canvas_width // p_width
    center_h_tile = (num_horizontal_tiles - 1) // 2

    # Place pattern tiles according to the alternating rule
    for v_tile in range(num_vertical_tiles):
        if v_tile % 2 == 0:
            # Even vertical tile: place in center
            h_tiles = [center_h_tile]
        else:
            # Odd vertical tile: place on left and right edges
            h_tiles = [0, num_horizontal_tiles - 1]

        for h_tile in h_tiles:
            # Copy pattern to this tile position
            for pr in range(p_height):
                for pc in range(p_width):
                    if pattern[pr][pc] == 1:
                        out_r = v_tile * p_height + pr
                        out_c = h_tile * p_width + pc
                        if out_r < canvas_height and out_c < canvas_width:
                            output[out_r][out_c] = 8

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("5833af48", solve)
