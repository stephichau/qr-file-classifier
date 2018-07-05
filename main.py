import json
API_KEY = None
INFO_DICT = None

def get_keys(path):
    with open(path, 'r') as file:
        file = json.load(file)
        API_KEY = file['API_KEY']['KEY']
        INFO_DICT = file['web']
