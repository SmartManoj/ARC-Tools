"""
ARC-AGI Task 281123b4 Solution

Pattern Analysis:
- Input: 4x19 grid with 4 sections (4x4 each) separated by columns of 3s
- Sections are located at columns: 0-3, 5-8, 10-13, 15-18
- Section colors: 8 (section 1), 5 (section 2), 9 (section 3), 4 (section 4)
- Output: 4x4 grid

Transformation Rule:
For each position (r,c) in the output:
1. Look at position (r,c) in all 4 input sections
2. Among the non-zero values, select the one with highest priority
3. Priority order: 9 > 4 > 8 > 5
"""

import json
import numpy as np


def extract_sections(grid):
    """Extract 4 sections separated by columns of 3s"""
    sections = []
    sections.append(grid[:, 0:4])    # Section 1 (columns 0-3, color 8)
    sections.append(grid[:, 5:9])    # Section 2 (columns 5-8, color 5)
    sections.append(grid[:, 10:14])  # Section 3 (columns 10-13, color 9)
    sections.append(grid[:, 15:19])  # Section 4 (columns 15-18, color 4)
    return sections


def solve_task(input_grid):
    """
    Solve the task by selecting the highest priority non-zero value
    at each position across all 4 sections.
    Priority: 9 > 4 > 8 > 5
    """
    # Priority order for color selection
    priority = {9: 3, 4: 2, 8: 1, 5: 0, 0: -1}

    sections = extract_sections(input_grid)
    output = np.zeros((4, 4), dtype=int)

    for r in range(4):
        for c in range(4):
            # Get values from all 4 sections at position (r,c)
            values = [sections[i][r, c] for i in range(4)]

            # Filter non-zero values and select highest priority
            non_zeros = [v for v in values if v != 0]
            if non_zeros:
                output[r, c] = max(non_zeros, key=lambda x: priority[x])
            else:
                output[r, c] = 0

    return output


# Load the task data
with open('../ARC-AGI/data/evaluation/281123b4.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("TASK 281123b4 - TESTING SOLUTION")
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

print(f"\nTraining Results: {'All correct!' if all_correct else 'Some failures'}")

# Test on test example
print("\n" + "=" * 80)
print("TEST EXAMPLE")
print("=" * 80)

test_input = np.array(data['test'][0]['input'])
test_expected = np.array(data['test'][0]['output'])
test_predicted = solve_task(test_input)

print("\nInput sections:")
sections = extract_sections(test_input)
for i, section in enumerate(sections):
    print(f"\nSection {i+1}:")
    print(section)

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
