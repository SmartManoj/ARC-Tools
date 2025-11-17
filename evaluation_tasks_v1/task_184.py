import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    Find a 3x3 template with 4s and apply transformations to matching regions.
    The pattern involves: identifying template, finding marker value, and applying
    flipped template pattern to high-marker-density windows.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find the template region (3x3 with most 4s)
    max_4s = -1
    template_r, template_c = -1, -1
    template_region = None

    for r in range(h - 2):
        for c in range(w - 2):
            region = [result[r+i][c:c+3] for i in range(3)]
            four_count = sum(row.count(4) for row in region)
            if four_count > max_4s:
                max_4s = four_count
                template_r, template_c = r, c
                template_region = region

    if template_region is None or max_4s <= 0:
        return result

    # Find marker value (most common non-4, non-0 in template)
    marker_value = None
    value_counts = {}
    for row in template_region:
        for val in row:
            if val != 4 and val != 0:
                value_counts[val] = value_counts.get(val, 0) + 1

    if not value_counts:
        return result

    marker_value = max(value_counts, key=value_counts.get)

    # Create the vertically flipped template
    template_flipped = template_region[::-1]

    # Get positions of 4s in the flipped template
    flipped_4_positions = set()
    for i in range(3):
        for j in range(3):
            if template_flipped[i][j] == 4:
                flipped_4_positions.add((i, j))

    # Apply transformation to high-marker windows
    for wr in range(h - 2):
        for wc in range(w - 2):
            if wr == template_r and wc == template_c:
                continue

            window = [result[wr+i][wc:wc+3] for i in range(3)]
            marker_count = sum(row.count(marker_value) for row in window)

            # Process windows with exactly 4+ markers
            if marker_count >= 4:
                # Fill non-marker cells that are adjacent to markers
                for i in range(3):
                    for j in range(3):
                        cell_value = window[i][j]
                        if cell_value == marker_value or cell_value == 4:
                            continue

                        # Check if cell is orthogonally adjacent to a marker
                        is_adjacent_to_marker = False
                        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < 3 and 0 <= nj < 3:
                                if window[ni][nj] == marker_value:
                                    is_adjacent_to_marker = True
                                    break

                        # Only fill corner positions if adjacent to markers
                        # (not edges or center)
                        is_corner = (i, j) in [(0, 0), (0, 2), (2, 0), (2, 2)]

                        # Fill only corners if adjacent to marker
                        if is_corner and is_adjacent_to_marker:
                            result[wr+i][wc+j] = 4

    return result


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("79369cc6", solve)
