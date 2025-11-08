from arc_tools.logger import logger
from arc_tools.plot import plot_grids
def list_strip(list, element):
    list = list.copy()
    while list and list[0] == element:
        list.pop(0)
    while list and list[-1] == element:
        list.pop()
    return list

def debug_output(grid, expected_output, output, window_title='result'):
    if grid.compare(output, silent=True):
        logger.info(f"Output is still the same as the input - No changes, idiot.")
        exit(1)
    # print which cells are different
    for row in range(len(expected_output)):
        for col in range(len(expected_output[0])):
            if (expected_value := expected_output[row][col]) != (actual_value := output[row][col]):
                logger.info(f"At {row =}, {col = }, {expected_value = } != {actual_value = }")
    plot_grids([grid, expected_output, output], show=1, titles=["Input", "Expected output", "Actual output"], name=window_title)
