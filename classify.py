import argparse
from log import cool_print_decoration
import os
from classifier.main import classify_tests
from sheets.main import main as get_student_data

"""
python3 classify.py
--sheets path_to_directory_students_from_sheets
--scans path_to_directory_of_scans
--results path_to_directory_of_results
--evaluation i1, i2, i3, exam
"""

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheets", action="store", dest="sheets_directory",help="Directory where sheets api information is going to be stored")
    parser.add_argument("--scans", action="store", dest="scans_directory",help="Directory where scans are stored")
    parser.add_argument("--results", action="store", dest="results_directory",help="Directory where results are going to be stored")
    parser.add_argument("--evaluation", action="store", dest="evaluation_name",help="Evaluation name: i1, i2, i3, exam")
    return parser.parse_args()

def path_exists(path):
    return os.path.exists(path)

def main():
    results = parse_arguments()
    """ if not results.sheets_directory or not results.scans_directory or not results.results_directory or not results.evaluation_name:
        error_message = "Invalid arguments. Missing either --sheets, --scans or --results or --evaluation_name."
        cool_print_decoration(error_message, 'alert')
    elif not (path_exists(results.sheets_directory) and path_exists(results.scans_directory) and path_exists(results.results_directory)):
        error_message = "Invalid path(s). Check --sheets, --scans or --results paths provided."
        cool_print_decoration(error_message, 'alert')

    else:
        SHEETS_PATH = results.sheets_directory
        EVALUATION_NAME = results.evaluation_name
        # Read students data
        # get_student_data(SHEETS_PATH, EVALUATION_NAME)
    """
    SHEETS_PATH = results.sheets_directory
    EVALUATION_NAME = results.evaluation_name
    get_student_data(SHEETS_PATH, EVALUATION_NAME)

if __name__ == "__main__":
    main()