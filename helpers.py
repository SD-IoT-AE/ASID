"""
ASID Utility Helper Functions
-----------------------------
Generic functions for data loading, time tracking, and common conversions.
"""

import json, os, time
import pandas as pd

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return json.load(f)

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        print(f"[helpers] CSV file {path} not found.")
        return pd.DataFrame()
