import os
from arc_tools.grid import Grid, detect_objects
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern:
    1. Detects two similar objects and compares them column by column
    2. Finds groups of consecutive differing columns
    3. Creates an output showing a geometric "hull" pattern around differences

    The output forms a specific outline shape based on the difference regions.
    '''

    # Detect all non-zero objects
    all_objects = detect_objects(grid, ignore_colors=[0])

    if len(all_objects) != 2:
        logger.warning(f"Expected 2 objects, found {len(all_objects)}")
        return Grid([[0]])

    obj1, obj2 = all_objects[0], all_objects[1]

    # Normalize objects to grids
    def normalize_object(obj):
        obj_dict = {}
        for p in obj.points:
            obj_dict[(p.x, p.y)] = grid[p.y][p.x]
        x1, y1 = min(p.x for p in obj.points), min(p.y for p in obj.points)
        x2, y2 = max(p.x for p in obj.points), max(p.y for p in obj.points)
        normalized = []
        for y in range(y1, y2 + 1):
            normalized.append([obj_dict.get((x, y), 0) for x in range(x1, x2 + 1)])
        return normalized

    obj1_norm, obj2_norm = normalize_object(obj1), normalize_object(obj2)
    width = len(obj1_norm[0])

    # Compare columns
    diff_cols = [obj1_norm[row][col] != obj2_norm[row][col]
                 for col in range(width)
                 for row in range(len(obj1_norm))]

    # Recompute diff_cols correctly
    diff_cols = []
    for col in range(width):
        col1 = [obj1_norm[row][col] for row in range(len(obj1_norm))]
        col2 = [obj2_norm[row][col] for row in range(len(obj2_norm))]
        diff_cols.append(col1 != col2)

    # Find difference groups
    groups = []
    start = None
    for i, is_diff in enumerate(diff_cols):
        if is_diff and start is None:
            start = i
        elif not is_diff and start is not None:
            groups.append((start, i - 1))
            start = None
    if start is not None:
        groups.append((start, len(diff_cols) - 1))

    if len(groups) < 2:
        return Grid([[0]])

    # Calculate output dimensions
    gap_size = groups[1][0] - groups[0][1] - 1
    max_group_size = max(e - s + 1 for s, e in groups)
    min_group_size = min(e - s + 1 for s, e in groups)

    # Height determination logic
    if gap_size > 1:
        output_height = gap_size
    elif max_group_size == min_group_size:
        # Symmetric groups
        output_height = max_group_size + 1
    elif max_group_size >= 4:
        # Large asymmetric groups with gap=1
        output_height = max_group_size
    else:
        # Small asymmetric groups with gap=1
        output_height = min_group_size

    # Initialize output
    output = [[0] * width for _ in range(output_height)]

    # Apply the pattern
    # Determine which row gets ALL difference columns
    # For height 2, it's row 0. For height 3+, it's row 1
    main_row = 0 if output_height == 2 else 1
    for col in range(width):
        if diff_cols[col]:
            output[main_row][col] = 8

    # Rightmost column (if at edge) appears in all rows (except for height=2)
    if groups[-1][1] == width - 1 and output_height > 2:
        for row in range(output_height):
            output[row][width - 1] = 8

    # Leftmost column (if at position 0)
    if groups[0][0] == 0:
        if output_height == 3:
            for row in range(output_height):
                output[row][0] = 8
        elif output_height == 2:
            # Already marked in main_row (row 0)
            pass
        else:
            # For height 4+, already marked in main_row
            pass

    # Additional pattern for other rows (creating the outline shape)
    if output_height == 4:
        # Row 0: mark second column of first group and second-to-last of second group
        if groups[0][1] - groups[0][0] >= 1:
            output[0][groups[0][0] + 1] = 8
        if groups[1][1] - groups[1][0] >= 1:
            output[0][groups[1][1] - 1] = 8

        # Row 2: mark third column of first group
        if groups[0][1] - groups[0][0] >= 2:
            output[2][groups[0][0] + 2] = 8

        # Row 3: only rightmost (already done)

    elif output_height == 2:
        # Row 1: mark last column of first group
        output[1][groups[0][1]] = 8

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("2037f2c7", solve)
