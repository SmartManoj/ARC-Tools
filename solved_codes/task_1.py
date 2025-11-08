# 00576224
import os
import getpass
if getpass.getuser() == 'root':
    os.chdir('/kaggle/working/ARC-Tools/workspace')
else:
    os.chdir(r'C:\Users\smart\Desktop\GD\ARC-Tools\workspace')
from collections import Counter
from arc_tools.grid import Grid, detect_objects, move_object
from arc_tools.logger import logger
from helper import solve_task

def transform(grid: Grid) -> Grid:
    output_height = grid.height * 3
    output_width = grid.width * 3
    new_grid_list = [[0] * output_width for _ in range(output_height)]

    for r in range(output_height):
        for c in range(output_width):
            source_r = r % grid.height
            source_c = c % grid.width

            if (r // grid.height) % 2 == 1:
                # Flipped block
                val = grid.get(grid.width - 1 - source_c, source_r)
            else:
                # Normal block
                val = grid.get(source_c, source_r)

            new_grid_list[r][c] = val

    result = Grid(new_grid_list)
    # end of logic
    return result

if __name__ == "__main__":
    solve_task(transform)
