"""
ARC-AGI Task 3194b014 Solution

Pattern Analysis:
- Input: 20x20 grid containing various colors and rectangular blocks
- Each input contains several solid rectangular blocks (filled with single color)
- Output: 3x3 grid filled with a single color

Transformation Rule:
1. Find all maximal solid rectangular blocks (minimum 3x3 size)
2. Select the block with the largest area
3. If there's a tie in area, choose the block with smallest column position (leftmost)
4. Output a 3x3 grid filled with that block's color
"""

import json
import numpy as np


def find_maximal_rectangles(grid, min_size=3):
    """
    Find all maximal solid rectangles in the grid.

    A maximal rectangle is a rectangle filled with the same color
    that is not contained within a larger rectangle at the same position.
    """
    rectangles = []
    rows, cols = grid.shape

    # Try every possible starting position
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0:
                continue

            color = grid[r, c]

            # Try all possible rectangle sizes from this position
            for h in range(min_size, rows - r + 1):
                for w in range(min_size, cols - c + 1):
                    if r + h > rows or c + w > cols:
                        continue

                    # Check if this region is a perfect rectangle of the same color
                    is_perfect = True
                    for i in range(r, r + h):
                        for j in range(c, c + w):
                            if grid[i, j] != color:
                                is_perfect = False
                                break
                        if not is_perfect:
                            break

                    if is_perfect:
                        rectangles.append({
                            'color': int(color),
                            'row': r,
                            'col': c,
                            'height': h,
                            'width': w,
                            'area': h * w
                        })

    # Keep only the maximal rectangle at each position (largest area)
    maximal_dict = {}
    for rect in rectangles:
        key = (rect['row'], rect['col'], rect['color'])
        if key not in maximal_dict or rect['area'] > maximal_dict[key]['area']:
            maximal_dict[key] = rect

    return list(maximal_dict.values())


def solve_task(input_grid):
    """
    Solve the task by finding the largest rectangle.
    Tie-breaker: choose the one with smallest column position (leftmost).
    Returns a 3x3 grid filled with the winning color.
    """
    rectangles = find_maximal_rectangles(input_grid)

    if not rectangles:
        # Fallback: return empty grid
        return np.zeros((3, 3), dtype=int)

    # Sort by: area (descending), then column (ascending), then row (ascending)
    rectangles.sort(key=lambda r: (-r['area'], r['col'], r['row']))

    # The first rectangle is the winner
    winner_color = rectangles[0]['color']

    # Return 3x3 grid filled with this color
    return np.full((3, 3), winner_color, dtype=int)


# Load the task data
with open('../ARC-AGI/data/evaluation/3194b014.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("TASK 3194b014 - TESTING SOLUTION")
print("=" * 80)

# Test on training examples
print("\nTraining Examples:")
all_correct = True
for i, example in enumerate(data['train']):
    input_grid = np.array(example['input'])
    expected_output = np.array(example['output'])
    predicted_output = solve_task(input_grid)

    is_correct = np.array_equal(predicted_output, expected_output)
    all_correct = all_correct and is_correct

    print(f"Example {i+1}: {'✓ PASS' if is_correct else '✗ FAIL'}")
    if not is_correct:
        print("Expected:")
        print(expected_output)
        print("Predicted:")
        print(predicted_output)

        # Show rectangles found
        rectangles = find_maximal_rectangles(input_grid)
        rectangles.sort(key=lambda r: (-r['area'], r['col'], r['row']))
        print("\nRectangles found (top 5):")
        for rect in rectangles[:5]:
            print(f"  Color {rect['color']}: {rect['height']}x{rect['width']} = {rect['area']} "
                  f"at ({rect['row']}, {rect['col']})")

print(f"\nTraining Results: {'All correct!' if all_correct else 'Some failures'}")

# Test on test example
print("\n" + "=" * 80)
print("TEST EXAMPLE")
print("=" * 80)

test_input = np.array(data['test'][0]['input'])
test_expected = np.array(data['test'][0]['output'])
test_predicted = solve_task(test_input)

print("\nRectangles found:")
rectangles = find_maximal_rectangles(test_input)
rectangles.sort(key=lambda r: (-r['area'], r['col'], r['row']))
for i, rect in enumerate(rectangles[:10]):
    print(f"{i+1}. Color {rect['color']}: {rect['height']}x{rect['width']} = {rect['area']:3d} "
          f"at ({rect['row']:2d}, {rect['col']:2d})")

print("\nExpected output:")
print(test_expected)

print("\nPredicted output:")
print(test_predicted)

is_correct = np.array_equal(test_predicted, test_expected)
print(f"\nTest Result: {'✓ PASS' if is_correct else '✗ FAIL'}")

if is_correct:
    print("\n" + "=" * 80)
    print("SUCCESS! Solution is correct.")
    print("=" * 80)
