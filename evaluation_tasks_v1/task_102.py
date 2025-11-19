import os
from arc_tools.grid import Grid
from helper import solve_task

def has_regular_pattern(section):
    """Check if a section has a regular alternating [2,2,2] and [2,0,2] pattern"""
    for i in range(len(section)):
        if i % 2 == 0:  # Even rows (0, 2, 4, ...)
            if section[i] != [2, 2, 2]:
                return False
        else:  # Odd rows (1, 3, 5, ...)
            if section[i] != [2, 0, 2]:
                return False
    return True

def solve(grid: Grid):
    """
    Transform the grid by shifting vertical sections based on patterns.

    The grid is divided into vertical sections of 3 columns each, separated by
    columns of 0s. The transformation depends on whether the last section has
    a regular alternating pattern:
    - If last section is regular and odd number of sections: swap first two sections
    - If last section is regular and even number of sections: swap middle two sections
    - If last section is not regular: rotate all sections left by 1
    """
    # Convert grid to list for easier manipulation
    input_data = [[cell for cell in row] for row in grid]
    num_rows = len(input_data)
    num_cols = len(input_data[0])

    # Identify separator columns (all 0s)
    separators = []
    for col in range(num_cols):
        if all(input_data[row][col] == 0 for row in range(num_rows)):
            separators.append(col)

    # Extract sections
    sections_bounds = []
    start = 0
    for sep in separators:
        if start < sep:
            sections_bounds.append((start, sep))
        start = sep + 1
    if start < num_cols:
        sections_bounds.append((start, num_cols))

    # Extract section data
    sections = []
    for start, end in sections_bounds:
        section_data = []
        for row in range(num_rows):
            section_data.append(input_data[row][start:end])
        sections.append(section_data)

    num_sections = len(sections)

    # Check if last section has regular pattern
    last_is_regular = has_regular_pattern(sections[-1])

    # Determine transformation
    if last_is_regular:
        if num_sections % 2 == 1:  # Odd number of sections
            # Swap first two sections
            output_sections = sections.copy()
            output_sections[0], output_sections[1] = sections[1], sections[0]
        else:  # Even number of sections
            # Swap middle two sections
            mid = num_sections // 2
            output_sections = sections.copy()
            output_sections[mid - 1], output_sections[mid] = sections[mid], sections[mid - 1]
    else:
        # Rotate all sections left by 1
        output_sections = [sections[(i - 1) % num_sections] for i in range(num_sections)]

    # Reconstruct the grid
    output_data = [[0] * num_cols for _ in range(num_rows)]

    for section_idx, (start, end) in enumerate(sections_bounds):
        section_data = output_sections[section_idx]
        for row in range(num_rows):
            for col_offset, col in enumerate(range(start, end)):
                output_data[row][col] = section_data[row][col_offset]

    # Restore separator columns
    for sep in separators:
        for row in range(num_rows):
            output_data[row][sep] = 0

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("42a15761", solve)
