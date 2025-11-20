#!/usr/bin/env python3
import json

with open('/home/user/ARC-AGI/data/evaluation/81c0276b.json') as f:
    data = json.load(f)

def analyze_example(input_grid, output_grid, name):
    print(f"\n{'='*60}")
    print(f"Analyzing {name}")
    print(f"{'='*60}")

    # Find separator color (appears as full rows/columns)
    grid = input_grid
    h, w = len(grid), len(grid[0])

    # Check all potential separator colors
    potential_seps = set()

    # Check for full rows
    for row in grid:
        if len(set(row)) == 1:
            potential_seps.add(row[0])

    # Find the separator color
    separator = None
    for color in potential_seps:
        if color == 0:
            continue
        # Check if this color fills entire rows/columns
        full_rows = [i for i in range(h) if all(grid[i][j] == color for j in range(w))]
        full_cols = [j for j in range(w) if all(grid[i][j] == color for i in range(h))]

        if full_rows and full_cols:
            separator = color
            print(f"Separator color: {separator}")
            print(f"Full rows at indices: {full_rows}")
            print(f"Full cols at indices: {full_cols}")
            break

    if not separator:
        print("Could not find separator")
        return

    # Extract cell boundaries
    full_rows = [i for i in range(h) if all(grid[i][j] == separator for j in range(w))]
    full_cols = [j for j in range(w) if all(grid[i][j] == separator for i in range(h))]

    # Get cell ranges
    row_boundaries = [-1] + full_rows + [h]
    col_boundaries = [-1] + full_cols + [w]

    cell_rows = []
    for i in range(len(row_boundaries) - 1):
        r_start = row_boundaries[i] + 1
        r_end = row_boundaries[i+1]
        if r_start < r_end:
            cell_rows.append((r_start, r_end))

    cell_cols = []
    for i in range(len(col_boundaries) - 1):
        c_start = col_boundaries[i] + 1
        c_end = col_boundaries[i+1]
        if c_start < c_end:
            cell_cols.append((c_start, c_end))

    print(f"Cell row ranges: {cell_rows}")
    print(f"Cell col ranges: {cell_cols}")

    # Extract the color from each cell
    cells = {}
    for ri, (r_start, r_end) in enumerate(cell_rows):
        for ci, (c_start, c_end) in enumerate(cell_cols):
            # Extract cell content
            cell_content = []
            for r in range(r_start, r_end):
                for c in range(c_start, c_end):
                    val = grid[r][c]
                    if val != 0 and val != separator:
                        cell_content.append(val)

            # Get the dominant non-background, non-separator color
            if cell_content:
                color = max(set(cell_content), key=cell_content.count)
            else:
                color = 0

            cells[(ri, ci)] = color

    print(f"\nCell grid ({len(cell_rows)} x {len(cell_cols)}):")
    for ri in range(len(cell_rows)):
        row_vals = [cells.get((ri, ci), 0) for ci in range(len(cell_cols))]
        print(f"  {row_vals}")

    # Analyze colors by column
    color_cols = {}
    for ri, ci in cells:
        color = cells[(ri, ci)]
        if color != 0 and color != separator:
            if color not in color_cols:
                color_cols[color] = set()
            color_cols[color].add(ci)

    print(f"\nColors and their columns:")
    for color in sorted(color_cols.keys()):
        cols = sorted(color_cols[color])
        count = len(cols)
        print(f"  Color {color}: columns {cols} (count: {count})")

    print(f"\nExpected output:")
    for row in output_grid:
        print(f"  {row}")

    print(f"\nAnalyzing output pattern:")
    print(f"  Output size: {len(output_grid)} x {len(output_grid[0]) if output_grid else 0}")
    print(f"  Number of unique colors: {len(color_cols)}")
    print(f"  Number of cell columns: {len(cell_cols)}")

# Analyze all training examples
for i, example in enumerate(data['train']):
    analyze_example(example['input'], example['output'], f"Training Example {i+1}")

# Analyze test example
print("\n" + "="*60)
print("TEST EXAMPLE")
print("="*60)
test = data['test'][0]
analyze_example(test['input'], test['output'], "Test Example")
