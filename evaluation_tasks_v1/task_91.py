import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Transforms 5x5 input with corner/cross/background colors into 10x10 output.

    The input has:
    - Corner color: appears at all 4 corners
    - Cross color: forms a plus/cross in the center
    - Background color: the remaining color

    Output is 10x10 divided into 4 quadrants:
    - Top-left (0-4, 0-4): Original input
    - Top-right (0-4, 5-9): Each row is [corner, cross, bg, corner, cross]
    - Bottom-left (5-9, 0-4): Rows filled with pattern [corner, cross, bg, corner, cross]
    - Bottom-right (5-9, 0-4): Diagonal stripe pattern

    The bottom-right quadrant follows: each diagonal (r-c constant) repeats the pattern
    [cross, bg, corner, cross, bg] with offset based on diagonal number.
    '''

    # Identify the three unique colors
    all_colors = set()
    for row in grid:
        all_colors.update(row)

    # Corner color appears at all 4 corners
    corner_color = grid[0][0]

    # Find cross color - appears in the center cross pattern
    # The cross consists of middle column and middle row
    center_colors = set()
    for r in range(5):
        center_colors.add(grid[r][2])  # Middle column
    for c in range(5):
        center_colors.add(grid[2][c])  # Middle row
    center_colors.discard(corner_color)  # Remove corner if present

    # The cross color should be the one that appears most in center positions
    # excluding the background
    cross_candidates = center_colors - {corner_color}

    # Count occurrences of each candidate in the cross
    cross_positions = [(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)]
    color_counts = {}
    for color in all_colors:
        if color != corner_color:
            count = sum(1 for r, c in cross_positions if grid[r][c] == color)
            color_counts[color] = count

    cross_color = max(color_counts, key=color_counts.get)

    # Background is the remaining color
    bg_color = (all_colors - {corner_color, cross_color}).pop()

    # Build the 10x10 output
    output = []

    # Top half (rows 0-4)
    for r in range(5):
        row = []
        # Top-left: original input
        for c in range(5):
            row.append(grid[r][c])
        # Top-right: [corner, cross, bg, corner, cross]
        row.extend([corner_color, cross_color, bg_color, corner_color, cross_color])
        output.append(row)

    # Bottom half (rows 5-9)
    # Pattern for rows: [corner, cross, bg, corner, cross]
    color_pattern = [corner_color, cross_color, bg_color, corner_color, cross_color]

    for row_idx in range(5):
        row = []
        # Bottom-left: each row filled with one color from pattern
        row_color = color_pattern[row_idx]
        row.extend([row_color] * 5)

        # Bottom-right: diagonal pattern
        # Each diagonal (where r-c is constant) follows pattern [cross, bg, corner, cross, bg]
        pattern = [cross_color, bg_color, corner_color, cross_color, bg_color]
        offset_map = [0, 2, 1, 0, 0]

        for col_idx in range(5):
            # Calculate diagonal number d = r - c + 4 (ranges 0-8)
            d = row_idx - col_idx + 4
            # Offset based on distance from center diagonal
            offset = offset_map[min(d, 8 - d)]
            # Position along this diagonal
            # Count how many cells with the same d value come before this one
            pos = 0
            for r2 in range(5):
                for c2 in range(5):
                    if r2 - c2 + 4 == d:
                        if r2 < row_idx or (r2 == row_idx and c2 < col_idx):
                            pos += 1
                        elif r2 == row_idx and c2 == col_idx:
                            break

            # Get color from pattern
            color = pattern[(offset + pos) % 5]
            row.append(color)

        output.append(row)

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("3979b1a8", solve)
