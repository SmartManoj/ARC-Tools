import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transforms a 3x3 grid into a 9x9 grid based on uniform rows/columns:
    - If a row has all same values: tile input horizontally 3x at that row position
    - If a column has all same values: tile input vertically 3x at that column position
    '''
    # Create 9x9 output filled with zeros
    output_data = [[0] * 9 for _ in range(9)]

    # Check for uniform rows
    for row_idx in range(3):
        row = [grid[row_idx][col] for col in range(3)]
        if len(set(row)) == 1:  # All elements are the same
            # Tile horizontally at this row position
            start_row = row_idx * 3
            for i in range(3):
                for col in range(9):
                    output_data[start_row + i][col] = grid[i][col % 3]
            return Grid(output_data)

    # Check for uniform columns
    for col_idx in range(3):
        col = [grid[row][col_idx] for row in range(3)]
        if len(set(col)) == 1:  # All elements are the same
            # Tile vertically at this column position
            start_col = col_idx * 3
            for row in range(9):
                for i in range(3):
                    output_data[row][start_col + i] = grid[row % 3][i]
            return Grid(output_data)

    # Default: return zeros if no pattern found
    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("15696249", solve)
