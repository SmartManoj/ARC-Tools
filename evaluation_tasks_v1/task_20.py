import os
from arc_tools.grid import Grid, Color
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Connects three colored markers (2=red, 3=green, 4=yellow) using gray lines (5).

    Pattern: Creates a rectilinear Steiner tree connecting the three points.
    The junction point can be the median, one of the colored points, or determined
    by the optimal routing strategy.
    '''
    # Find the three colored points
    points = {}
    for r in range(grid.height):
        for c in range(grid.width):
            color = grid[r][c]
            if color in [2, 3, 4]:
                points[color] = (r, c)

    if len(points) != 3:
        return grid.copy()

    # Extract points and sort by row
    all_points = [points[2], points[3], points[4]]
    sorted_points = sorted(all_points, key=lambda p: (p[0], p[1]))

    # Calculate median row and column
    rows = sorted([p[0] for p in all_points])
    cols = sorted([p[1] for p in all_points])
    median_row = rows[1]
    median_col = cols[1]

    # Create output grid as copy of input
    output = grid.copy()

    # Helper function to draw line
    def draw_line(r1, c1, r2, c2):
        if r1 == r2:  # Horizontal line
            for c in range(min(c1, c2), max(c1, c2) + 1):
                if output[r1][c] == 0:
                    output[r1][c] = 5
        elif c1 == c2:  # Vertical line
            for r in range(min(r1, r2), max(r1, r2) + 1):
                if output[r][c1] == 0:
                    output[r][c1] = 5

    # Check which points are on the median row/column
    on_median_row = [p for p in all_points if p[0] == median_row]
    on_median_col = [p for p in all_points if p[1] == median_col]

    # Determine connection strategy
    # Check if using a colored point as hub would be better (smaller row+col sum)
    min_point_sum = min(p[0] + p[1] for p in all_points)
    median_sum = median_row + median_col

    # Use median junction if points are on axes AND no colored point is very close to origin
    # If a colored point has a very small row+col sum (<= 2, indicating it's at or near (0,0) or (1,1)), use it as hub
    use_median_junction = len(on_median_row) >= 1 and len(on_median_col) >= 1 and min_point_sum > 2

    if use_median_junction:
        # Use median as junction - connect all points toward (median_row, median_col)
        for point in all_points:
            r, c = point
            if r == median_row and c == median_col:
                continue  # Already at median
            elif r == median_row:
                # Horizontal line to median
                draw_line(r, c, median_row, median_col)
            elif c == median_col:
                # Vertical line to median
                draw_line(r, c, median_row, median_col)
            else:
                # L-shaped path to median - create rectangular connection
                # Draw both paths: one through median column, one through current column
                if on_median_row:
                    target_col = on_median_row[0][1]
                    # Heuristic: if current row is above median row, route through the point on median row
                    # UNLESS the current column is very close to the median column (within 2 cells)
                    # Otherwise, route to median column and also ensure full rectangular connection
                    if r < median_row:
                        # Above median row: check if close to median column
                        if abs(c - median_col) <= 1:
                            # Close to median column: route to median column
                            draw_line(r, c, r, median_col)
                            draw_line(r, median_col, median_row, median_col)
                            # Also draw path at current column if different
                            if c != median_col:
                                draw_line(r, c, median_row, c)
                                draw_line(median_row, c, median_row, median_col)
                        else:
                            # Far from median column: route through target column
                            draw_line(r, c, r, target_col)
                            draw_line(r, target_col, median_row, target_col)
                    else:
                        # Below median row: create rectangular path
                        # Horizontal from current to median column at current row
                        draw_line(r, c, r, median_col)
                        # Vertical at current column from current row to median row
                        draw_line(r, c, median_row, c)
                        # Vertical at median column from current row to median row
                        draw_line(r, median_col, median_row, median_col)
                        # Horizontal at median row from current column to target column (point on median row)
                        draw_line(median_row, c, median_row, target_col)
                else:
                    # Route to median column first, then to median row
                    draw_line(r, c, r, median_col)
                    draw_line(r, median_col, median_row, median_col)
    else:
        # Use a colored point as hub (the one with smallest row+col sum)
        hub = min(all_points, key=lambda p: p[0] + p[1])
        hub_r, hub_c = hub

        # Connect other points to hub
        for point in all_points:
            if point == hub:
                continue
            r, c = point

            # L-shaped path to hub
            # Choose direction that creates cleaner paths
            if abs(r - hub_r) >= abs(c - hub_c):
                # Horizontal first
                draw_line(r, c, r, hub_c)
                draw_line(r, hub_c, hub_r, hub_c)
            else:
                # Vertical first
                draw_line(r, c, hub_r, c)
                draw_line(hub_r, c, hub_r, hub_c)

    return output

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("0e671a1a", solve)
