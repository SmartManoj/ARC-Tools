def create_prompt(data):
    prompt = fr"""
class GridPoint:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

class GridRegion:
    attr x1, y1, x2, y2

class Grid(SafeList):
    def __init__(self, grid: list[list[int]], background_color: int | None = None,...)

class SubGrid(Grid):
    def __init__(self, region: GridRegion, parent_grid: Grid, obj_color: int | None = None, points: list[GridPoint] | None = None):
        attr region, 
        points : list[GridPoint] -> list of points in the subgrid

Find the transformation rule for the following input and output.
Input: {data['train'][0]['input']}
Output: {data['train'][0]['output']}

API reference:
- Grid class: Grid(2d_list) - create a grid from a 2D list
- grid.get(x, y) - get value at position (x, y)
- detect_objects(grid) - return list of SubGrids (detects connected components)
- SubGrid.points - list of GridPoint objects in order

CRITICAL RULES:
0. Don't view this file because it is too large to fit in the context.
"/kaggle/working/ARC-Tools/arc_tools/grid.py"
1. Do NOT hardcode dimensions or positions
2. ALWAYS return Grid object: Grid([[val1], [val2], ...])
3. Keep solution SIMPLE - prefer 2-3 lines
4. Look for spatial patterns (straighten, align) not just color counting
5. For shape transformations, use object.points directly
6. All points in the SubGrid may not have the same value.
7. Input and Output are Grid Objects (2D list)

Core Rules:
1) Rows correspond to the y-axis and columns to the x-axis
grid.get(x, y) is equivalent to grid[y][x] (grid[row][col])

Steps:
1) Complete the function in the following file and run it
C:\Users\smart\Desktop\GD\ARC-Tools\workspace\task.py

2) Run the function and make it pass the train tasks.

"""
    with open('prompt.txt', 'w') as f:
        f.write(prompt)

WORKSPACE_DIR=r'C:\Users\smart\Desktop\GD\ARC-Tools\workspace'
import json
path=r'C:\Users\smart\Desktop\arc-prize-2024\arc-agi_evaluation_challenges.json'
with open(path, 'r') as file:
    test_data = json.load(file)

task_number = int(open('task_number.txt').read())
for task_id, data in list(test_data.items())[task_number-1:task_number]:
    print(task_id)
    with open(f'{WORKSPACE_DIR}/data.json', 'w') as file:
        json.dump(data, file)
    create_prompt(data)
    break