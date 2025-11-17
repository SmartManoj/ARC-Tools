#!/usr/bin/env python3
import json
from arc_tools.grid import Grid

with open('/home/user/ARC-AGI/data/evaluation/81c0276b.json') as f:
    data = json.load(f)

# Import the solve function
import sys
sys.path.insert(0, '/home/user/ARC-Tools/evaluation_tasks_v1')
from task_196 import solve

# Test on all training examples
print("Testing Training Examples:")
for i, example in enumerate(data['train']):
    input_grid = Grid(example['input'])
    expected = example['output']
    result = solve(input_grid)
    result_list = [list(row) for row in result]

    matches = result_list == expected
    status = "✓ PASS" if matches else "✗ FAIL"
    print(f"\nExample {i+1}: {status}")
    print(f"Expected: {expected}")
    print(f"Got:      {result_list}")

# Test on test example
print("\n" + "="*60)
print("Testing Test Example:")
test = data['test'][0]
input_grid = Grid(test['input'])
expected = test['output']
result = solve(input_grid)
result_list = [list(row) for row in result]

matches = result_list == expected
status = "✓ PASS" if matches else "✗ FAIL"
print(f"{status}")
print(f"Expected: {expected}")
print(f"Got:      {result_list}")
