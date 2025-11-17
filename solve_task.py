#!/usr/bin/env python3
"""
Script to solve ARC tasks by downloading data from the ARC-AGI-2 repository
and attempting to find the solution pattern.
"""

import sys
import json
import os
import urllib.request
from pathlib import Path
from arc_tools.grid import Grid
from arc_tools.logger import logger

# Base URL for ARC-AGI-2 data
ARC_REPO_BASE = "https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/data"

def download_task_data(task_id):
    """Download task data from the ARC-AGI-2 repository."""
    # Try evaluation dataset first, then training dataset
    for split in ['evaluation', 'training']:
        url = f"{ARC_REPO_BASE}/{split}/{task_id}.json"
        try:
            logger.info(f"Downloading {split} task: {url}")
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                logger.info(f"Successfully downloaded {split} task {task_id}")
                return data
        except Exception as e:
            logger.debug(f"Failed to download from {split}: {e}")
            continue

    raise FileNotFoundError(f"Could not find task data for {task_id}")

def solve_task(task_id):
    """Solve a task given its ID."""
    logger.info(f"Solving task: {task_id}")

    # Download task data
    try:
        data = download_task_data(task_id)
    except Exception as e:
        logger.error(f"Failed to download task data: {e}")
        return False

    # Log task information
    num_train = len(data.get('train', []))
    num_test = len(data.get('test', []))
    logger.info(f"Task has {num_train} training examples and {num_test} test examples")

    # Try to solve the task
    # For now, just validate that we have the data structure
    if 'train' not in data or 'test' not in data:
        logger.error("Invalid task data structure")
        return False

    # Log training examples
    for idx, train_example in enumerate(data['train'], 1):
        input_grid = Grid(train_example['input'])
        output_grid = Grid(train_example['output'])
        logger.info(f"Train example {idx}: input {input_grid.shape} -> output {output_grid.shape}")

    # Log test examples
    for idx, test_example in enumerate(data['test'], 1):
        input_grid = Grid(test_example['input'])
        logger.info(f"Test example {idx}: input {input_grid.shape}")
        if 'output' in test_example:
            output_grid = Grid(test_example['output'])
            logger.info(f"  Expected output: {output_grid.shape}")

    logger.info(f"Task {task_id} processing complete")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python solve_task.py <task_id>")
        sys.exit(1)

    task_id = sys.argv[1]
    success = solve_task(task_id)
    sys.exit(0 if success else 1)
