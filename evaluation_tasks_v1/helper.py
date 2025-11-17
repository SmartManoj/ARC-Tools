from arc_tools.grid import Grid, detect_objects, move_object
from arc_tools.logger import logger
from arc_tools.utils import debug_output
import json
def solve_task(task_id, task_fn):
    import os
    # Get the base directory - go up from evaluation_tasks_v1 to ARC-Tools
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Then go to parent directory to find ARC-AGI-2
    arc_dir = os.path.join(os.path.dirname(base_dir), 'ARC-AGI-2', 'data')

    # Try evaluation first, then training
    for dataset in ['evaluation', 'training']:
        file = os.path.join(arc_dir, dataset, f'{task_id}.json')
        try:
            with open(file, 'r') as f:
                content = f.read()
                # Skip if file contains 404 error
                if '404: Not Found' in content:
                    continue
                data = json.loads(content)
            break
        except FileNotFoundError:
            continue
    else:
        raise FileNotFoundError(f"Could not find {task_id}.json in evaluation or training")
    train_data = data['train']
    test_data = data['test']
    is_passed = False
    for task_idx, task in enumerate(train_data, 1):
        grid = Grid(task['input'])
        output = task_fn(grid)
        expected_output = Grid(task['output'])
        if not output.compare(expected_output):
            logger.info(f"Train Task {task_idx} failed")
            debug_output(grid, expected_output, output)
            break
        logger.info(f"Train Task {task_idx} passed")
    else:
        is_passed = True
    if is_passed:
        outputs = []
        for task_idx, task in enumerate(test_data, 1):
            output = task_fn(Grid(task['input']))
            outputs.append({"attempt_1": output, "attempt_2": output})
            logger.info(f"Test Task {task_idx} output successfully generated")
        with open('output.json', 'w') as file:
            json.dump(outputs, file)
    