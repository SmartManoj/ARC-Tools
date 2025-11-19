import os
from arc_tools.grid import Grid
from collections import Counter
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Denoising a tiled/repeating pattern.

    The input contains repeating blocks with noise. The task is to:
    1. Identify block boundaries (they're separated by mostly-zero regions)
    2. For each position within a block, gather all values from corresponding
       positions across all block instances
    3. Use majority voting (mode) to determine the clean value
    4. Reconstruct the output with the cleaned repeating pattern
    '''

    # Analyze the grid to find block structure
    block_info = find_block_structure(grid)

    if block_info is None:
        # Fallback: return grid as-is if we can't find structure
        return Grid(grid.data)

    row_groups, col_groups = block_info

    # Create output grid
    output_data = [[0] * grid.width for _ in range(grid.height)]

    # For each block position, collect values and compute mode
    for row_group in row_groups:
        for col_group in col_groups:
            # Collect values from all blocks at each position within this block
            block_height = row_group[1] - row_group[0]
            block_width = col_group[1] - col_group[0]

            for dr in range(block_height):
                for dc in range(block_width):
                    values = []
                    # Gather values from all block instances
                    for rg in row_groups:
                        for cg in col_groups:
                            r = rg[0] + dr
                            c = cg[0] + dc
                            if r < grid.height and c < grid.width:
                                values.append(grid[r][c])

                    # Use mode to determine clean value
                    if values:
                        counter = Counter(values)
                        clean_value = counter.most_common(1)[0][0]

                        # Set this value in all corresponding positions in output
                        r = row_group[0] + dr
                        c = col_group[0] + dc
                        if r < grid.height and c < grid.width:
                            output_data[r][c] = clean_value

    return Grid(output_data)


def find_block_structure(grid: Grid):
    '''
    Find the structure of repeating blocks in the grid.

    Returns: (row_groups, col_groups) where each group is a list of (start, end) tuples
    representing the positions of content blocks (not separators).
    '''

    # Find row groups (content rows separated by mostly-zero rows)
    row_groups = find_groups_in_dimension(grid, is_row=True)

    # Find column groups (content columns separated by mostly-zero columns)
    col_groups = find_groups_in_dimension(grid, is_row=False)

    if not row_groups or not col_groups:
        return None

    return (row_groups, col_groups)


def find_groups_in_dimension(grid: Grid, is_row: bool):
    '''
    Find groups of content (non-separator) rows or columns.

    Returns: List of (start, end) tuples for each group.
    '''
    size = grid.height if is_row else grid.width

    # Determine which rows/columns are mostly zeros (separators)
    is_separator = []
    for i in range(size):
        if is_row:
            values = [grid[i][c] for c in range(grid.width)]
        else:
            values = [grid[r][i] for r in range(grid.height)]

        zero_count = sum(1 for v in values if v == 0)
        total = len(values)
        # Consider it a separator if >80% zeros
        is_separator.append(zero_count / total > 0.8)

    # Find groups of consecutive non-separator rows/columns
    groups = []
    in_group = False
    start = 0

    for i in range(size):
        if not is_separator[i] and not in_group:
            # Start of a new group
            start = i
            in_group = True
        elif is_separator[i] and in_group:
            # End of current group
            groups.append((start, i))
            in_group = False

    # Handle case where last group extends to end
    if in_group:
        groups.append((start, size))

    # Verify groups have consistent sizes (they should for repeating blocks)
    if len(groups) > 1:
        # Check if all groups have the same size
        sizes = [end - start for start, end in groups]
        if len(set(sizes)) == 1:
            return groups
        else:
            # Use the most common size and filter groups
            counter = Counter(sizes)
            expected_size = counter.most_common(1)[0][0]
            filtered_groups = [g for g in groups if g[1] - g[0] == expected_size]
            return filtered_groups if filtered_groups else groups

    return groups


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("0607ce86", solve)
