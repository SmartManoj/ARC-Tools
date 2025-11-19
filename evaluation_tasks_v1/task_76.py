import os
from arc_tools.grid import Grid, detect_objects
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern:
    1. The grid contains 2 rectangular regions filled with 0s (black)
    2. One region (marker region) has only a single colored marker cell
    3. The other region (pattern region) has a pattern of 4s plus the same colored marker
    4. Output size matches the marker region size
    5. The pattern is placed in the output aligned by the marker positions
    '''
    # Find all objects (0-filled rectangular regions)
    objects = detect_objects(grid)

    if len(objects) != 2:
        logger.error(f"Expected 2 objects, found {len(objects)}")
        return grid

    # Identify marker region vs pattern region
    obj1, obj2 = objects[0], objects[1]

    # Count colored cells (non-0, non-background) in each object
    def count_colored_cells(obj):
        count = 0
        positions = []
        for r in range(obj.height):
            for c in range(obj.width):
                if obj[r][c] != 0 and obj[r][c] != grid.background_color:
                    count += 1
                    positions.append((r, c, obj[r][c]))
        return count, positions

    count1, cells1 = count_colored_cells(obj1)
    count2, cells2 = count_colored_cells(obj2)

    # Determine which is marker region (1 cell) and which is pattern region (multiple cells)
    if count1 == 1 and count2 > 1:
        marker_region = obj1
        pattern_region = obj2
        marker_pos = cells1[0][:2]  # (row, col)
        marker_color = cells1[0][2]
        pattern_cells = cells2
    elif count2 == 1 and count1 > 1:
        marker_region = obj2
        pattern_region = obj1
        marker_pos = cells2[0][:2]  # (row, col)
        marker_color = cells2[0][2]
        pattern_cells = cells1
    else:
        logger.error(f"Could not identify marker and pattern regions")
        return grid

    # Find marker position in pattern region
    pattern_marker_pos = None
    for r, c, color in pattern_cells:
        if color == marker_color:
            pattern_marker_pos = (r, c)
            break

    if pattern_marker_pos is None:
        logger.error(f"Could not find marker in pattern region")
        return grid

    # Create output grid with marker region dimensions
    output_height = marker_region.height
    output_width = marker_region.width
    output_data = [[0 for _ in range(output_width)] for _ in range(output_height)]

    # Calculate offset to align markers
    # pattern_marker_pos is where marker is in pattern
    # marker_pos is where it should be in output
    offset_r = marker_pos[0] - pattern_marker_pos[0]
    offset_c = marker_pos[1] - pattern_marker_pos[1]

    # Place pattern cells in output
    for r, c, color in pattern_cells:
        new_r = r + offset_r
        new_c = c + offset_c

        # Only place if within bounds
        if 0 <= new_r < output_height and 0 <= new_c < output_width:
            output_data[new_r][new_c] = color

    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("2f0c5170", solve)
