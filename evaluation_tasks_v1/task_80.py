import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Find all maximal rectangular blocks of 0s (at least 2x2) and convert them to 1s

    Algorithm:
    1. Find all maximal rectangles of 0s using a greedy approach
    2. For rectangles with dimensions >= 2x2, mark those cells with 1
    '''
    # Create a copy of the grid
    output_data = [row[:] for row in grid]
    h = len(grid)
    w = len(grid[0])

    # Track which cells have been assigned to a rectangle
    marked = [[False] * w for _ in range(h)]

    def find_rectangle(start_r, start_c):
        """Find the largest valid rectangle (>=2x2) of 0s starting from (start_r, start_c)"""
        if grid[start_r][start_c] != 0 or marked[start_r][start_c]:
            return None

        # Find max width at starting row
        max_width = 0
        for c in range(start_c, w):
            if grid[start_r][c] == 0 and not marked[start_r][c]:
                max_width += 1
            else:
                break

        if max_width == 0:
            return None

        # Try all possible width and height combinations
        # Prioritize rectangles that are at least 2x2
        best_area = 0
        best_width = 0
        best_height = 0

        for width in range(1, max_width + 1):
            height = 0
            for r in range(start_r, h):
                can_extend = True
                for c in range(start_c, start_c + width):
                    if grid[r][c] != 0 or marked[r][c]:
                        can_extend = False
                        break
                if can_extend:
                    height = r - start_r + 1
                else:
                    break

            area = width * height
            # Prioritize rectangles that are at least 2x2
            if width >= 2 and height >= 2:
                if area > best_area:
                    best_area = area
                    best_width = width
                    best_height = height

        # If we found a valid rectangle (>=2x2), return it
        if best_area > 0:
            return (start_r, start_c, best_height, best_width)

        return None

    # Find all rectangles greedily
    rectangles = []

    for r in range(h):
        for c in range(w):
            if grid[r][c] == 0 and not marked[r][c]:
                rect = find_rectangle(r, c)
                if rect:
                    start_r, start_c, rect_h, rect_w = rect
                    rectangles.append(rect)
                    # Mark these cells
                    for rr in range(start_r, start_r + rect_h):
                        for cc in range(start_c, start_c + rect_w):
                            marked[rr][cc] = True

    # Apply the rectangles to output
    for start_r, start_c, rect_h, rect_w in rectangles:
        for r in range(start_r, start_r + rect_h):
            for c in range(start_c, start_c + rect_w):
                output_data[r][c] = 1

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("31adaf00", solve)
