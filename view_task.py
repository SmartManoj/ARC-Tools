#!/usr/bin/env python3
"""
Script to download and view ARC task data.
"""
import sys
import json
import urllib.request

ARC_REPO_BASE = "https://raw.githubusercontent.com/arcprize/ARC-AGI-2/main/data"

def download_task_data(task_id):
    """Download task data from the ARC-AGI-2 repository."""
    for split in ['evaluation', 'training']:
        url = f"{ARC_REPO_BASE}/{split}/{task_id}.json"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                return data
        except Exception:
            continue
    raise FileNotFoundError(f"Could not find task data for {task_id}")

if __name__ == "__main__":
    task_id = sys.argv[1]
    data = download_task_data(task_id)
    print(json.dumps(data, indent=2))
