import json
import os
import shutil
from .cool_prints import cool_print_decoration

def classify_tests_with_qr(sheet_txt_file_path, qr_txt_file_path, results_path, evaluation_name):
    sheet_data = None
    with open(sheet_txt_file_path, 'r') as sheet_txt:
        sheet_data = json.load(sheet_txt)
    
    qr_data = None
    with open(qr_txt_file_path, 'r') as qr_txt:
        qr_data = json.load(qr_txt)

    for student_name in sheet_data:
        student_directory = '{}/{}'.format(results_path, student_name)
        if not os.path.exists(student_directory):
            os.mkdir(student_directory)
        for student_qr_number in sheet_data[student_name]:

            # Check if qr_data has number assigned to student
            if not (qr_data.get(student_qr_number)):
                continue

            files_path_array = qr_data[student_qr_number]
            for file_path in files_path_array:
                file_path_split = file_path.split('/')
                filename = '{}_{}'.format(evaluation_name, file_path_split[-1])
                # file_path_split[-1] = filename
                file_path = '/'.join(file_path_split)
                cool_print_decoration(f'Moving file from {file_path} to {student_directory}', style='info')
                try:
                    shutil.move(file_path, student_directory)
                except Exception as e:
                    cool_print_decoration('Error moving file: {}'.format(e), style='alert')
                else:
                    cool_print_decoration('File successfully moved!', style='result')

if __name__ == '__main__':
    pass