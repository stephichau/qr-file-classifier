import json
import os

def check_file(_path: str) -> bool:
    return os.path.exists(_path)

def read_data(path: str) -> dict:
    with open(path, 'r') as f:
        _data = json.load(f)
    return _data