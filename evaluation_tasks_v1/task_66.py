import os
from arc_tools.grid import Grid, detect_objects
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Create a staircase output based on counting colored rectangular objects

    1. Detect all single-color rectangular objects (ignoring black/0 background)
    2. Count how many objects exist for each color
    3. Sort colors by their object count (descending)
    4. Create output grid where:
       - Number of rows = number of distinct colors
       - Width = maximum count across all colors
       - Row i: (max_count - count[i]) leading zeros + count[i] cells of that color

    This creates a triangular/staircase pattern.
    '''
    # Detect all single-color objects, ignoring black background
    objects = detect_objects(grid, single_color_only=True, ignore_colors=[0])

    # Count objects by color
    color_counts = {}
    for obj in objects:
        color = obj.color
        if color is not None and color != 0:
            if color not in color_counts:
                color_counts[color] = 0
            color_counts[color] += 1

    # Sort colors by count (descending)
    sorted_colors = sorted(color_counts.keys(), key=lambda c: color_counts[c], reverse=True)

    # Get max count for determining output width
    max_count = max(color_counts.values()) if color_counts else 0

    # Build output grid (staircase pattern)
    output_data = []
    for color in sorted_colors:
        count = color_counts[color]
        # Row has (max_count - count) leading zeros, followed by count cells of the color
        row = [0] * (max_count - count) + [color] * count
        output_data.append(row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("2753e76c", solve)
