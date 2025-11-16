import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Analyzes scattered horizontal and vertical lines in the input and creates
    a nested rectangular pattern in the output.

    Pattern:
    1. Find all horizontal and vertical lines (consecutive pixels of same color)
    2. For each color, determine the maximum line length (horizontal or vertical)
    3. Sort colors by their line lengths (descending)
    4. Create a square output grid with size = longest line length
    5. Fill concentric rectangular frames from outside to inside, where each
       color fills a frame based on its sorted position
    '''
    color_lengths = {}

    # Find horizontal lines
    for r in range(grid.height):
        c = 0
        while c < grid.width:
            if grid[r][c] != 0:
                color = grid[r][c]
                start_c = c
                while c < grid.width and grid[r][c] == color:
                    c += 1
                length = c - start_c
                color_lengths[color] = max(color_lengths.get(color, 0), length)
            else:
                c += 1

    # Find vertical lines
    for c in range(grid.width):
        r = 0
        while r < grid.height:
            if grid[r][c] != 0:
                color = grid[r][c]
                start_r = r
                while r < grid.height and grid[r][c] == color:
                    r += 1
                length = r - start_r
                color_lengths[color] = max(color_lengths.get(color, 0), length)
            else:
                r += 1

    # Sort colors by their maximum line length (descending)
    sorted_colors = sorted(color_lengths.items(), key=lambda x: x[1], reverse=True)

    # Create output grid with size = longest line length
    max_length = sorted_colors[0][1]
    output_data = [[0] * max_length for _ in range(max_length)]

    # Fill concentric rectangular frames
    # Each color fills a frame at distance 'layer' from the edge
    for layer, (color, length) in enumerate(sorted_colors):
        # Fill the rectangular frame at this layer
        for i in range(layer, max_length - layer):
            output_data[layer][i] = color  # Top edge
            output_data[max_length - 1 - layer][i] = color  # Bottom edge
            output_data[i][layer] = color  # Left edge
            output_data[i][max_length - 1 - layer] = color  # Right edge

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("3ee1011a", solve)
