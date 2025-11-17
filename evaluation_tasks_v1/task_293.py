import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Rotate a line of red cells around a gray pivot point.
    Find gray (5) cells with adjacent red (2) cells in one direction.
    Convert the red cells to green (3) and place new red cells
    in the perpendicular direction, maintaining the same length.
    '''
    result = grid.copy()

    # Find gray (5) cells
    for r in range(grid.height):
        for c in range(grid.width):
            if grid[r, c] == Color.GRAY:
                # Check all four directions for red cells
                directions = [
                    (-1, 0, 'up'),    # up
                    (1, 0, 'down'),   # down
                    (0, -1, 'left'),  # left
                    (0, 1, 'right')   # right
                ]

                for dr, dc, direction in directions:
                    # Count consecutive red cells in this direction
                    red_cells = []
                    rr, cc = r + dr, c + dc
                    while 0 <= rr < grid.height and 0 <= cc < grid.width and grid[rr, cc] == Color.RED:
                        red_cells.append((rr, cc))
                        rr += dr
                        cc += dc

                    if red_cells:
                        # Convert red cells to green
                        for rr, cc in red_cells:
                            result[rr, cc] = Color.GREEN

                        # Place new red cells in perpendicular direction
                        # Determine perpendicular direction (opposite side of gray cell)
                        if direction == 'up':
                            # Place red cells going down from gray
                            for i in range(len(red_cells)):
                                nr, nc = r + i + 1, c
                                if 0 <= nr < grid.height:
                                    result[nr, nc] = Color.RED
                        elif direction == 'down':
                            # Place red cells going up from gray
                            for i in range(len(red_cells)):
                                nr, nc = r - i - 1, c
                                if 0 <= nr >= 0:
                                    result[nr, nc] = Color.RED
                        elif direction == 'left':
                            # Place red cells going right from gray
                            for i in range(len(red_cells)):
                                nr, nc = r, c + i + 1
                                if 0 <= nc < grid.width:
                                    result[nr, nc] = Color.RED
                        elif direction == 'right':
                            # Place red cells going left from gray
                            for i in range(len(red_cells)):
                                nr, nc = r, c - i - 1
                                if 0 <= nc >= 0:
                                    result[nr, nc] = Color.RED

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("c074846d", solve)
