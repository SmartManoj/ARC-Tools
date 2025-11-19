import os
from arc_tools.grid import Grid, Color
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Grid is divided into tiles by separator rows/columns (all same value).
    Some tiles have cells marked with 8. The transformation finds all tiles that
    match the same base pattern and applies the 8 markings to all of them.

    Algorithm:
    1. Detect separator rows/columns (rows/cols where all values are the same)
    2. Extract tiles between separators
    3. Find tiles containing 8s and their base pattern (8s replaced with expected values)
    4. For each tile with 8s, find all tiles matching the base pattern
    5. Apply 8 markings to all matching tiles
    '''
    height = len(grid)
    width = len(grid[0])

    # Find separator rows (rows where all values are the same)
    sep_rows = []
    for r in range(height):
        if len(set(grid[r])) == 1:
            sep_rows.append(r)

    # Find separator columns
    sep_cols = []
    for c in range(width):
        col_vals = [grid[r][c] for r in range(height)]
        if len(set(col_vals)) == 1:
            sep_cols.append(c)

    # Create tile boundaries
    tile_row_ranges = []
    prev = 0
    for sep in sep_rows:
        if sep > prev:
            tile_row_ranges.append((prev, sep))
        prev = sep + 1
    if prev < height:
        tile_row_ranges.append((prev, height))

    tile_col_ranges = []
    prev = 0
    for sep in sep_cols:
        if sep > prev:
            tile_col_ranges.append((prev, sep))
        prev = sep + 1
    if prev < width:
        tile_col_ranges.append((prev, width))

    # Extract all tiles and find tiles with 8s
    tiles_with_8s = []
    all_tiles = {}

    for i, (r_start, r_end) in enumerate(tile_row_ranges):
        for j, (c_start, c_end) in enumerate(tile_col_ranges):
            tile = []
            has_8 = False
            for r in range(r_start, r_end):
                row = []
                for c in range(c_start, c_end):
                    val = grid[r][c]
                    row.append(val)
                    if val == 8:
                        has_8 = True
                tile.append(row)

            all_tiles[(i, j)] = (tile, r_start, r_end, c_start, c_end)
            if has_8:
                tiles_with_8s.append((i, j))

    # Create output grid as copy of input
    output = [[grid[r][c] for c in range(width)] for r in range(height)]

    # For each tile with 8s, find matching tiles and apply 8s
    for tile_idx in tiles_with_8s:
        tile_with_8, r_start, r_end, c_start, c_end = all_tiles[tile_idx]

        tile_height = len(tile_with_8)
        tile_width = len(tile_with_8[0]) if tile_height > 0 else 0


        # Find positions where 8s appear
        positions_with_8 = []
        for r in range(tile_height):
            for c in range(tile_width):
                if tile_with_8[r][c] == 8:
                    positions_with_8.append((r, c))

        # Create base pattern (8s replaced with what they would be in matching tiles)
        # Find a matching tile of the same dimensions without 8s
        base_pattern = None
        for other_idx, (other_tile, _, _, _, _) in all_tiles.items():
            if other_idx == tile_idx:
                continue

            # Must have same dimensions
            if len(other_tile) != tile_height or len(other_tile[0]) != tile_width:
                continue

            # Must not have 8s
            has_8 = any(other_tile[r][c] == 8 for r in range(tile_height) for c in range(tile_width))
            if has_8:
                continue

            # Check if patterns match (treating 8 as wildcard in tile_with_8)
            # Also check that all 8-positions have the same value in other_tile
            matches = True
            expected_8_value = None
            for r in range(tile_height):
                for c in range(tile_width):
                    tile_val = tile_with_8[r][c]
                    other_val = other_tile[r][c]

                    if tile_val == 8:
                        # At 8 positions, check they all have the same value
                        if expected_8_value is None:
                            expected_8_value = other_val
                        elif other_val != expected_8_value:
                            matches = False
                            break
                    else:
                        # At non-8 positions, values must match exactly
                        if tile_val != other_val:
                            matches = False
                            break
                if not matches:
                    break

            if matches:
                base_pattern = other_tile
                break

        if base_pattern is None:
            # No matching base pattern found
            # Try a fallback: match tiles where some rows match exactly
            # and the row with 8s matches a row that's all the same value

            # Find which rows have all 8s
            all_8_rows = []
            for r in range(tile_height):
                if all(tile_with_8[r][c] == 8 for c in range(tile_width)):
                    all_8_rows.append(r)

            if len(all_8_rows) > 0:
                # Try to find tiles where ANY row matches ANY row in the tile with 8s
                for other_idx, (other_tile, or_start, or_end, oc_start, oc_end) in all_tiles.items():
                    if other_idx == tile_idx:
                        continue
                    if len(other_tile) != tile_height or len(other_tile[0]) != tile_width:
                        continue

                    # Check how many rows in other_tile match any row in tile_with_8
                    # Count each matching row in other_tile (including duplicates)
                    matching_rows_in_other = 0
                    for r2 in range(tile_height):
                        row2 = [other_tile[r2][c] for c in range(tile_width)]
                        for r1 in range(tile_height):
                            if r1 in all_8_rows:
                                continue
                            row1 = [tile_with_8[r1][c] for c in range(tile_width)]
                            if row1 == row2:
                                matching_rows_in_other += 1
                                break  # Count this other_tile row once

                    # Require at least 2 matching rows in the other tile
                    if matching_rows_in_other >= 2:
                        # Determine what value 8 replaces by checking other tiles
                        # Look for a tile with all same value at 8-row positions
                        # Only check tiles with same dimensions
                        target_value = None
                        for check_idx, (check_tile, _, _, _, _) in all_tiles.items():
                            if check_idx == tile_idx:
                                continue
                            if len(check_tile) != tile_height or len(check_tile[0]) != tile_width:
                                continue
                            for r in all_8_rows:
                                if len(check_tile) <= r:
                                    continue
                                row = [check_tile[r][c] for c in range(tile_width)]
                                if len(set(row)) == 1 and row[0] != 8:
                                    target_value = row[0]
                                    break
                            if target_value is not None:
                                break

                        # Apply 8s only to rows that have all the target value
                        for r in range(tile_height):
                            other_row = [other_tile[r][c] for c in range(tile_width)]
                            if len(set(other_row)) == 1 and other_row[0] == target_value:
                                for c in range(tile_width):
                                    output[or_start + r][oc_start + c] = 8
            continue

        # Apply 8s to all tiles matching the base pattern (including those that already have 8s)
        for other_idx, (other_tile, or_start, or_end, oc_start, oc_end) in all_tiles.items():
            # Must have same dimensions
            if len(other_tile) != tile_height or len(other_tile[0]) != tile_width:
                continue

            # Check if this tile matches the base pattern (allowing 8s at the marked positions)
            matches = True
            for r in range(tile_height):
                for c in range(tile_width):
                    other_val = other_tile[r][c]
                    base_val = base_pattern[r][c]

                    # At positions where 8s should be, accept either the base value or 8
                    if (r, c) in positions_with_8:
                        if other_val != base_val and other_val != 8:
                            matches = False
                            break
                    else:
                        # At other positions, must match base pattern exactly
                        if other_val != base_val:
                            matches = False
                            break
                if not matches:
                    break

            if matches:
                # Apply 8s to this tile
                for r, c in positions_with_8:
                    output[or_start + r][oc_start + c] = 8

    return Grid(output)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("4ff4c9da", solve)
