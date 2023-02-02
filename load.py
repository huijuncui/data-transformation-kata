#!/usr/bin/env python3

import json
import time, os

def output_to_json(j, mrn):
    output_path = f"data/out/{int(time.time())}/patient_{mrn}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as fp:
        json.dump(j, fp, indent=4)