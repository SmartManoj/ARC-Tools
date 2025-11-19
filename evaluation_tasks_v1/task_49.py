import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Restores a corrupted repeating pattern by filling in zeros.

    The grid has a repeating tile pattern. The tile size varies and must be detected.
    We try different period candidates and choose the one with most consistent values.
    '''
    from collections import Counter

    height = len(grid)
    width = len(grid[0])

    # Try different tile periods and score them by consistency
    def score_period(period_h, period_w):
        """Score how consistent the pattern is with this period"""
        consistency_score = 0
        total_positions = 0

        for tile_i in range(period_h):
            for tile_j in range(period_w):
                # Collect all non-zero values at this tile position
                values = []
                for i in range(tile_i, height, period_h):
                    for j in range(tile_j, width, period_w):
                        if grid[i][j] != 0:
                            values.append(grid[i][j])

                if values:
                    total_positions += 1
                    # Count most common value
                    most_common_count = Counter(values).most_common(1)[0][1]
                    consistency_score += most_common_count / len(values)

        return consistency_score / max(total_positions, 1)

    # Try period candidates from 2 to 15
    best_height = height
    best_width = width
    best_score = 0

    for period_h in range(2, min(height, 15)):
        for period_w in range(2, min(width, 15)):
            score = score_period(period_h, period_w)
            if score > best_score:
                best_score = score
                best_height = period_h
                best_width = period_w

    tile_height = best_height
    tile_width = best_width

    # Create output grid (copy of input)
    output_data = []
    for row in grid:
        output_data.append(list(row))

    # For each zero cell, find the correct value from the pattern
    for i in range(height):
        for j in range(width):
            if grid[i][j] == 0:
                # Find the position within the repeating tile
                tile_i = i % tile_height
                tile_j = j % tile_width

                # Collect all non-zero values at this position in the pattern
                values = []
                for check_i in range(tile_i, height, tile_height):
                    for check_j in range(tile_j, width, tile_width):
                        val = grid[check_i][check_j]
                        if val != 0:
                            values.append(val)

                # Use the most common non-zero value (should be consistent across the pattern)
                if values:
                    most_common = Counter(values).most_common(1)[0][0]
                    output_data[i][j] = most_common

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("1d0a4b61", solve)
