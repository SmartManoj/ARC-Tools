import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task
import numpy as np

def solve(grid: Grid):
    '''
    Pattern: Find a shape made of 8s in the input, then find all instances
    of that same shape (in any rotation) made of 3s, and replace those 3s with 8s.

    Steps:
    1. Extract the pattern formed by all 8s in the grid
    2. Generate all 4 rotations (0°, 90°, 180°, 270°) of this pattern
    3. For each rotation, search the grid for instances where 3s form that exact shape
    4. Replace those 3s with 8s
    '''
    # Convert to numpy array for easier manipulation
    arr = np.array([[int(cell) for cell in row] for row in grid])

    # Find all positions with value 8
    eight_positions = np.argwhere(arr == 8)

    if len(eight_positions) == 0:
        return grid

    # Get the bounding box of 8s
    min_r, min_c = eight_positions.min(axis=0)
    max_r, max_c = eight_positions.max(axis=0)

    # Extract the pattern (relative coordinates)
    pattern = set()
    for r, c in eight_positions:
        pattern.add((r - min_r, c - min_c))

    # Generate all 4 rotations of the pattern
    rotations = [pattern]

    # 90° clockwise rotation: (r, c) -> (c, height-1-r)
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # 90° clockwise
    pattern_90 = set()
    for r, c in pattern:
        pattern_90.add((c, height - 1 - r))
    rotations.append(pattern_90)

    # 180° rotation: (r, c) -> (height-1-r, width-1-c)
    pattern_180 = set()
    for r, c in pattern:
        pattern_180.add((height - 1 - r, width - 1 - c))
    rotations.append(pattern_180)

    # 270° clockwise (90° counter-clockwise): (r, c) -> (width-1-c, r)
    pattern_270 = set()
    for r, c in pattern:
        pattern_270.add((width - 1 - c, r))
    rotations.append(pattern_270)

    # Search for each rotation pattern in the grid where 3s form the shape
    result = arr.copy()

    for rot_pattern in rotations:
        # Get bounding box of this rotation
        if len(rot_pattern) == 0:
            continue

        rot_list = list(rot_pattern)
        rot_min_r = min(r for r, c in rot_list)
        rot_max_r = max(r for r, c in rot_list)
        rot_min_c = min(c for r, c in rot_list)
        rot_max_c = max(c for r, c in rot_list)

        rot_height = rot_max_r - rot_min_r + 1
        rot_width = rot_max_c - rot_min_c + 1

        # Normalize pattern to start at (0, 0)
        normalized_pattern = set()
        for r, c in rot_pattern:
            normalized_pattern.add((r - rot_min_r, c - rot_min_c))

        # Search the entire grid for this pattern made of 3s
        for start_r in range(arr.shape[0] - rot_height + 1):
            for start_c in range(arr.shape[1] - rot_width + 1):
                # Check if the pattern matches at this position
                matches = True
                for r, c in normalized_pattern:
                    if arr[start_r + r, start_c + c] != 3:
                        matches = False
                        break

                if matches:
                    # Additional check: make sure ALL positions in the bounding box
                    # that should be 3 (according to pattern) are actually 3,
                    # and positions not in pattern don't interfere
                    valid = True
                    for r, c in normalized_pattern:
                        abs_r = start_r + r
                        abs_c = start_c + c
                        if arr[abs_r, abs_c] != 3:
                            valid = False
                            break

                    if valid:
                        # Replace these 3s with 8s
                        for r, c in normalized_pattern:
                            result[start_r + r, start_c + c] = 8

    # Convert back to Grid
    output_data = [[int(cell) for cell in row] for row in result]
    return Grid(output_data)

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("50f325b5", solve)
