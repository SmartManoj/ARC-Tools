import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    For each rectangular region filled with a uniform color that contains one marker pixel
    of a different color, transform the interior by:
    1. Keeping the border intact
    2. Filling the interior with a symmetric diamond/X pattern using the marker color
    3. Setting all other interior cells to 0 (black)
    '''
    result = grid.copy()

    # Find all non-black regions
    visited = set()
    h, w = len(grid), len(grid[0])

    for start_r in range(h):
        for start_c in range(w):
            if (start_r, start_c) in visited or grid[start_r][start_c] == 0:
                continue

            # Flood fill to find connected region
            main_color = grid[start_r][start_c]
            region = []
            stack = [(start_r, start_c)]

            while stack:
                r, c = stack.pop()
                if (r, c) in visited or r < 0 or r >= h or c < 0 or c >= w:
                    continue
                if grid[r][c] != main_color and grid[r][c] != 0:
                    # Found a different non-black color in this region
                    region.append((r, c, grid[r][c]))
                    visited.add((r, c))
                    continue
                if grid[r][c] != main_color:
                    continue

                visited.add((r, c))
                region.append((r, c, main_color))

                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    stack.append((r + dr, c + dc))

            # Find bounding box and colors
            rows = [r for r, c, _ in region]
            cols = [c for r, c, _ in region]
            min_row, max_row = min(rows), max(rows)
            min_col, max_col = min(cols), max(cols)

            # Count colors
            color_counts = {}
            for r, c, color in region:
                color_counts[color] = color_counts.get(color, 0) + 1

            # Check if this is a rectangle with one marker
            if len(color_counts) < 2:
                continue

            sorted_colors = sorted(color_counts.items(), key=lambda x: x[1])
            marker_color = sorted_colors[0][0]
            border_color = sorted_colors[-1][0]

            # Calculate interior dimensions
            height = max_row - min_row + 1
            width = max_col - min_col + 1
            interior_height = height - 2
            interior_width = width - 2

            if interior_height <= 0 or interior_width <= 0:
                continue

            # Fill interior with 0 first
            for r in range(min_row + 1, max_row):
                for c in range(min_col + 1, max_col):
                    result[r][c] = 0

            # Create diamond pattern
            # Hollow diamond, but middle row(s) fill horizontally
            max_row_dist = interior_height // 2

            for i in range(interior_height):
                row_min_dist = min(i, interior_height - 1 - i)

                left_col = row_min_dist
                right_col = interior_width - 1 - row_min_dist

                # At the middle row(s), fill horizontally from left_col to right_col
                # Otherwise, place only where col_min_dist == row_min_dist (diamond outline)
                if row_min_dist == max_row_dist:
                    for j in range(left_col, right_col + 1):
                        result[min_row + 1 + i][min_col + 1 + j] = marker_color
                else:
                    for j in range(interior_width):
                        col_min_dist = min(j, interior_width - 1 - j)
                        if col_min_dist == row_min_dist:
                            result[min_row + 1 + i][min_col + 1 + j] = marker_color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("8cb8642d", solve)
