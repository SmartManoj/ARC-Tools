#!/usr/bin/env python3
"""Generate task files for tasks 201-250"""

import os

# Task mapping for tasks 201-250
tasks = [
    (201, "8597cfd7"), (202, "85b81ff1"), (203, "85fa5666"), (204, "8719f442"),
    (205, "88207623"), (206, "891232d6"), (207, "896d5239"), (208, "8a371977"),
    (209, "8b28cd80"), (210, "8ba14f53"), (211, "8cb8642d"), (212, "8dae5dfc"),
    (213, "8e2edd66"), (214, "8ee62060"), (215, "8fbca751"), (216, "90347967"),
    (217, "903d1b4a"), (218, "9110e3c5"), (219, "917bccba"), (220, "929ab4e9"),
    (221, "92e50de0"), (222, "9356391f"), (223, "93b4f4b3"), (224, "93c31fbe"),
    (225, "94133066"), (226, "94414823"), (227, "94be5b80"), (228, "95a58926"),
    (229, "963f59bc"), (230, "96a8c0cd"), (231, "97239e3d"), (232, "9772c176"),
    (233, "981571dc"), (234, "992798f6"), (235, "99306f82"), (236, "9a4bb226"),
    (237, "9b2a60aa"), (238, "9b365c51"), (239, "9b4c17c4"), (240, "9bebae7a"),
    (241, "9c1e755f"), (242, "9c56f360"), (243, "9caba7c3"), (244, "9ddd00f0"),
    (245, "9def23fe"), (246, "9f27f097"), (247, "a04b2602"), (248, "a096bf4d"),
    (249, "a3f84088"), (250, "a406ac07")
]

template = """import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    add the function description first.
    '''
    objects = detect_objects(grid)

    return grid

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("{task_id}", solve)
"""

# Create evaluation_tasks_v1 directory if it doesn't exist
os.makedirs("evaluation_tasks_v1", exist_ok=True)

# Generate files
for task_num, task_id in tasks:
    filename = f"evaluation_tasks_v1/task_{task_num}.py"
    content = template.format(task_id=task_id)
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Created {filename}")

print(f"\nSuccessfully created {len(tasks)} task files!")
