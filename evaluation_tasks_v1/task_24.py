import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern Recognition:
    - Rows with 5 in the first column (column 0) are template rows
    - Extract template patterns from these rows (columns 1 onwards)
    - Empty rows (all zeros) are filled by cycling through templates
    - Non-empty rows without 5 in column 0 are kept as-is
    - Template rows themselves are kept as-is

    Example:
    Input:  [5, 0, 6, 0, 0]  <- template row 0: template is [0, 6, 0, 0]
            [5, 4, 4, 4, 0]  <- template row 1: template is [4, 4, 4, 0]
            [0, 0, 6, 0, 0]  <- non-empty, kept as-is
            [0, 0, 0, 0, 0]  <- empty, filled with [0] + template 0 = [0, 0, 6, 0, 0]
            [0, 0, 0, 0, 0]  <- empty, filled with [0] + template 1 = [0, 4, 4, 4, 0]
    '''
    height = grid.height
    width = grid.width

    # Step 1: Identify template rows (rows with 5 in column 0)
    template_rows = []
    templates = []

    for row_idx in range(height):
        if grid[row_idx][0] == 5:
            template_rows.append(row_idx)
            # Extract template: columns 1 onwards
            template = [grid[row_idx][col] for col in range(1, width)]
            templates.append(template)

    # Step 2: Build output grid
    output_data = []
    template_idx = 0  # Counter for cycling through templates

    for row_idx in range(height):
        row = [grid[row_idx][col] for col in range(width)]

        # Check if this row is all zeros (empty row)
        is_empty = all(cell == 0 for cell in row)

        if is_empty:
            # Fill with template: [0] + template[template_idx % len(templates)]
            new_row = [0] + templates[template_idx % len(templates)]
            output_data.append(new_row)
            template_idx += 1
        else:
            # Keep the row as-is (whether it has 5 or other content)
            output_data.append(row)

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("12422b43", solve)
