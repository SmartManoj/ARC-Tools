import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task


def solve(grid: Grid):
    '''
    Transformation pattern:
    1. Detect rectangular frames (hollow rectangles) in the input
    2. Identify scattered colors (non-zero, non-frame colors)
    3. Count occurrences of each scattered color
    4. Match frames to colors by sorting:
       - Frames by interior area (ascending)
       - Colors by occurrence count (ascending)
    5. Fill each frame's interior with a checkerboard pattern using its matched color
    6. Set all other pixels to 0
    '''

    # Detect rectangular frames
    frames = []

    # Try to find frames by detecting objects and checking if they're hollow rectangles
    for color in range(1, 10):
        # Find all cells of this color
        cells = []
        for r in range(grid.height):
            for c in range(grid.width):
                if grid[r][c] == color:
                    cells.append((r, c))

        if not cells:
            continue

        # Check if cells form a rectangular frame
        min_r = min(r for r, c in cells)
        max_r = max(r for r, c in cells)
        min_c = min(c for r, c in cells)
        max_c = max(c for r, c in cells)

        # A frame should have cells on the border of the rectangle
        is_frame = False
        if max_r > min_r and max_c > min_c:
            # Check if it forms a hollow rectangle
            border_cells = set()
            for r in range(min_r, max_r + 1):
                border_cells.add((r, min_c))
                border_cells.add((r, max_c))
            for c in range(min_c, max_c + 1):
                border_cells.add((min_r, c))
                border_cells.add((max_r, c))

            # A proper frame should have:
            # 1. Most cells on the border
            # 2. At least 8 cells (minimum viable rectangle frame)
            # 3. At least 50% of the border filled
            cells_on_border = len(set(cells) & border_cells)
            border_coverage = cells_on_border / len(border_cells) if len(border_cells) > 0 else 0

            if (len(cells) >= 8 and
                cells_on_border >= len(cells) * 0.8 and
                border_coverage >= 0.5):
                is_frame = True
                interior_height = max_r - min_r - 1
                interior_width = max_c - min_c - 1
                if interior_height > 0 and interior_width > 0:
                    frames.append({
                        'color': color,
                        'min_r': min_r,
                        'max_r': max_r,
                        'min_c': min_c,
                        'max_c': max_c,
                        'area': interior_height * interior_width
                    })

    # Get frame colors
    frame_colors = set(f['color'] for f in frames)

    # Count scattered colors (non-zero, non-frame colors)
    color_counts = {}
    for r in range(grid.height):
        for c in range(grid.width):
            color = grid[r][c]
            if color != 0 and color not in frame_colors:
                color_counts[color] = color_counts.get(color, 0) + 1

    # Sort frames by area
    frames_sorted = sorted(frames, key=lambda f: f['area'])

    # Sort colors by count
    colors_sorted = sorted(color_counts.items(), key=lambda x: x[0])
    colors_sorted = sorted(colors_sorted, key=lambda x: x[1])

    # Create mapping: frame -> fill color
    frame_to_color = {}
    for i, frame in enumerate(frames_sorted):
        if i < len(colors_sorted):
            frame_to_color[frame['color']] = colors_sorted[i][0]

    # Create output grid
    output = Grid([[0] * grid.width for _ in range(grid.height)])

    # Draw frames and fill with checkerboard pattern
    for frame in frames:
        frame_color = frame['color']
        fill_color = frame_to_color.get(frame_color, 0)

        # Draw frame border
        for r in range(frame['min_r'], frame['max_r'] + 1):
            output[r][frame['min_c']] = frame_color
            output[r][frame['max_c']] = frame_color
        for c in range(frame['min_c'], frame['max_c'] + 1):
            output[frame['min_r']][c] = frame_color
            output[frame['max_r']][c] = frame_color

        # Fill interior with checkerboard pattern
        # The pattern depends on whether the interior start position has even or odd sum
        interior_start_r = frame['min_r'] + 1
        interior_start_c = frame['min_c'] + 1
        start_parity = (interior_start_r + interior_start_c) % 2

        for r in range(interior_start_r, frame['max_r']):
            for c in range(interior_start_c, frame['max_c']):
                # Checkerboard: alternating pattern based on position
                if (r + c) % 2 == start_parity:
                    output[r][c] = fill_color
                else:
                    output[r][c] = 0

    return output


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("df8cc377", solve)
