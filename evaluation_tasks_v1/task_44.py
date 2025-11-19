import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Find rectangular borders and extract the largest interior

    1. Detect all rectangular borders made of a single color
    2. Find the rectangle with the largest interior area
    3. Extract and return the interior contents (excluding border)
    '''
    height = grid.height
    width = grid.width
    rectangles = []

    # Search for rectangular borders of each color (1-9)
    for color in range(1, 10):
        seen = set()
        for r1 in range(height):
            for c1 in range(width):
                if grid[r1][c1] == color:
                    # Try to find rectangles starting from this point
                    for r2 in range(r1 + 2, height):
                        for c2 in range(c1 + 2, width):
                            if (r1, c1, r2, c2) in seen:
                                continue

                            # Check if this forms a complete rectangle border
                            is_rectangle = True

                            # Check top and bottom edges
                            for c in range(c1, c2 + 1):
                                if grid[r1][c] != color or grid[r2][c] != color:
                                    is_rectangle = False
                                    break

                            # Check left and right edges
                            if is_rectangle:
                                for r in range(r1 + 1, r2):
                                    if grid[r][c1] != color or grid[r][c2] != color:
                                        is_rectangle = False
                                        break

                            if is_rectangle:
                                # Verify interior has at least some non-border cells
                                has_different = False
                                for r in range(r1 + 1, r2):
                                    for c in range(c1 + 1, c2):
                                        if grid[r][c] != color:
                                            has_different = True
                                            break
                                    if has_different:
                                        break

                                if has_different:
                                    seen.add((r1, c1, r2, c2))
                                    interior_area = (r2 - r1 - 1) * (c2 - c1 - 1)
                                    rectangles.append({
                                        'r1': r1,
                                        'c1': c1,
                                        'r2': r2,
                                        'c2': c2,
                                        'area': interior_area
                                    })

    # Find the rectangle with the largest interior area
    if rectangles:
        largest = max(rectangles, key=lambda r: r['area'])

        # Extract the interior contents
        interior = []
        for r in range(largest['r1'] + 1, largest['r2']):
            row = []
            for c in range(largest['c1'] + 1, largest['c2']):
                row.append(grid[r][c])
            interior.append(row)

        return Grid(interior)

    # Fallback: return empty grid if no rectangles found
    return Grid([[0]])

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("1a6449f1", solve)
