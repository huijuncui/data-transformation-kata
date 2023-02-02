#!/usr/bin/env python3

import json
import sys
import time, os

def output_to_json(j, mrn):
    output_path = f"data/out/{int(time.time())}/patient_{mrn}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        fp = open(output_path, 'w')
    except OSError:
        print("Could not open/write file:", output_path)
        sys.exit()

    with fp:
        json.dump(j, fp, indent=4)

# Move failed file (no mrn) to failed path
def output_to_failure(dir):
    error_path = f"data/error/{dir[8:]}"
    os.makedirs(os.path.dirname(error_path), exist_ok=True)
    os.rename(dir, error_path)
