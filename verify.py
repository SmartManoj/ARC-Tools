import enum
import json
import os
path=r'C:\Users\smart\Desktop\arc-prize-2024\arc-agi_evaluation_solutions.json'
with open(path, 'r') as file:
    test_data = json.load(file)

test_data_list = list(test_data.keys())
task_number = int(open('task_number.txt').read())
task_id = test_data_list[task_number-1]
tests = (test_data[task_id])
with open(r'C:\Users\smart\Desktop\GD\ARC-Tools\workspace\output.json', 'r') as file:
    solution = json.load(file)

for k, test in enumerate(tests):
    if test != solution[k]['attempt_1']:
        print(f'Task {task_id} test {k+1} failed')
        exit()

sol_file=r'C:\Users\smart\Desktop\GD\ARC-Tools\workspace\task.py'

solved_folder=r'C:\Users\smart\Desktop\GD\ARC-Tools\solved_codes'
with open(os.path.join(solved_folder, f'task_{task_number}.py'), 'w') as file:
    code = open(sol_file, 'r').read()

    file.write(f'# {task_id}\n' + code)
