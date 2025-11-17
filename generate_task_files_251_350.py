#!/usr/bin/env python3
"""Generate task files for tasks 251-350"""

import os

# Task mapping for tasks 251-350
tasks = [
    (251, "a57f2f04"), (252, "a59b95c0"), (253, "a680ac02"), (254, "a8610ef7"),
    (255, "a934301b"), (256, "aa18de87"), (257, "aa300dc3"), (258, "aa4ec2a5"),
    (259, "aab50785"), (260, "ac0c5833"), (261, "ac2e8ecf"), (262, "ac3e2b04"),
    (263, "ac605cbb"), (264, "ad7e01d0"), (265, "ae58858e"), (266, "aee291af"),
    (267, "af22c60d"), (268, "af24b4cc"), (269, "b0722778"), (270, "b0f4d537"),
    (271, "b15fca0b"), (272, "b1fc8b8e"), (273, "b20f7c8b"), (274, "b457fec5"),
    (275, "b4a43f3b"), (276, "b7999b51"), (277, "b7cb93ac"), (278, "b7f8a4d8"),
    (279, "b7fb29bc"), (280, "b942fd60"), (281, "b9630600"), (282, "ba9d41b8"),
    (283, "baf41dbf"), (284, "bb52a14b"), (285, "bbb1b8b6"), (286, "bc4146bd"),
    (287, "bcb3040b"), (288, "bd14c3bf"), (289, "be03b35f"), (290, "bf32578f"),
    (291, "bf699163"), (292, "bf89d739"), (293, "c074846d"), (294, "c1990cce"),
    (295, "c3202e5a"), (296, "c35c1b4c"), (297, "c48954c1"), (298, "c62e2108"),
    (299, "c64f1187"), (300, "c658a4bd"), (301, "c663677b"), (302, "c6e1b8da"),
    (303, "c7d4e6ad"), (304, "c87289bb"), (305, "c8b7cc0f"), (306, "c92b942c"),
    (307, "c97c0139"), (308, "ca8de6ea"), (309, "ca8f78db"), (310, "cad67732"),
    (311, "cb227835"), (312, "ccd554ac"), (313, "cd3c21df"), (314, "ce039d91"),
    (315, "ce8d95cc"), (316, "cf133acc"), (317, "cfb2ce5a"), (318, "d017b73f"),
    (319, "d19f7514"), (320, "d282b262"), (321, "d2acf2cb"), (322, "d304284e"),
    (323, "d37a1ef5"), (324, "d47aa2ff"), (325, "d492a647"), (326, "d4b1c2b1"),
    (327, "d4c90558"), (328, "d56f2372"), (329, "d5c634a2"), (330, "d931c21c"),
    (331, "d94c3b52"), (332, "da2b0fe3"), (333, "da515329"), (334, "dc2aa30b"),
    (335, "dc2e9a9d"), (336, "dd2401ed"), (337, "de493100"), (338, "df8cc377"),
    (339, "e0fb7511"), (340, "e133d23d"), (341, "e1baa8a4"), (342, "e1d2900e"),
    (343, "e2092e0c"), (344, "e21a174a"), (345, "e345f17b"), (346, "e4075551"),
    (347, "e41c6fd3"), (348, "e57337a4"), (349, "e5790162"), (350, "e5c44e8f")
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
