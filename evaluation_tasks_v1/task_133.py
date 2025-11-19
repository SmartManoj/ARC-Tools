import os
from arc_tools.grid import Grid, GridPoint
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Connect markers with diagonal lines
    1. Find all positions with value 1 (endpoints)
    2. Find all positions with value 6 (ray sources)
    3. For each pair of 1s, draw a diagonal line connecting them
    4. For each 6, draw diagonal rays in all four diagonal directions to edges
    '''
    # Create output grid as copy of input
    output_data = [[grid[r][c] for c in range(grid.width)] for r in range(grid.height)]
    height = grid.height
    width = grid.width

    # Find all 1s and 6s
    ones = []
    sixes = []

    for r in range(height):
        for c in range(width):
            if grid[r][c] == 1:
                ones.append((r, c))
            elif grid[r][c] == 6:
                sixes.append((r, c))

    # Track which 6s are on diagonal paths between 1s
    sixes_on_diagonal = set()

    # Connect pairs of 1s with diagonal lines
    for i in range(len(ones)):
        for j in range(i + 1, len(ones)):
            r1, c1 = ones[i]
            r2, c2 = ones[j]

            # Determine direction
            dr = 1 if r2 > r1 else -1
            dc = 1 if c2 > c1 else -1

            # Check if they can be connected diagonally
            if abs(r2 - r1) == abs(c2 - c1):
                # Draw diagonal line
                r, c = r1, c1
                while (r, c) != (r2, c2):
                    # Mark 6s that are on this diagonal path
                    if output_data[r][c] == 6:
                        sixes_on_diagonal.add((r, c))
                    else:
                        output_data[r][c] = 1
                    r += dr
                    c += dc
                # Place endpoint
                if output_data[r2][c2] != 6:
                    output_data[r2][c2] = 1

    # Extend diagonal rays only from 6s that are on diagonal paths
    for r, c in sixes_on_diagonal:
        # Four diagonal directions: NE, NW, SE, SW
        directions = [(-1, 1), (-1, -1), (1, 1), (1, -1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while 0 <= nr < height and 0 <= nc < width:
                # Stop if we encounter a 1
                if output_data[nr][nc] == 1:
                    break
                # Draw the ray
                output_data[nr][nc] = 6
                nr += dr
                nc += dc

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("55783887", solve)
