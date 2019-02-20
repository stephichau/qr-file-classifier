"""
Before running program, run setup.py to test if all the requirements are met
"""

from testing.setup import read_requirements

if __name__ == '__main__':
    _req_path = 'requirements.txt'
    read_requirements(_req_path)