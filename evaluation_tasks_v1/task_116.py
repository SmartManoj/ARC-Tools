import os
from arc_tools.grid import Grid
from helper import solve_task

def solve(grid: Grid):
    '''
    Solves a 4x4 Latin square puzzle where:
    - Each row must contain exactly the values 1, 2, 3, 4
    - Each column must contain exactly the values 1, 2, 3, 4
    - 0 represents empty cells that need to be filled

    This is like a simplified Sudoku for a 4x4 grid.
    '''
    # Convert grid to a mutable 2D list
    result = [[int(cell) for cell in row] for row in grid]
    height, width = len(result), len(result[0])

    def get_possible_values(row, col):
        """Get possible values for a cell at (row, col)"""
        # Values already in the row
        row_values = set(result[row])
        # Values already in the column
        col_values = set(result[r][col] for r in range(height))
        # Possible values are 1-4 minus those already used
        possible = {1, 2, 3, 4} - row_values - col_values
        return possible

    def solve_recursive():
        """Recursively solve the puzzle using backtracking"""
        # Find the first empty cell (value 0)
        for row in range(height):
            for col in range(width):
                if result[row][col] == 0:
                    # Try each possible value
                    possible = get_possible_values(row, col)
                    for value in possible:
                        result[row][col] = value
                        if solve_recursive():
                            return True
                        result[row][col] = 0  # Backtrack
                    return False
        return True  # All cells filled

    solve_recursive()
    return Grid(result)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("4cd1b7b2", solve)
