import os
from .separate_scans import separate_pdf_pages, save_qr_data_to_file
from .classify_with_qr import classify_tests_with_qr

STUDENTS_FILE_TXT_NAME = 'students_and_qr.txt'

def classify_tests(path_to_original_scans, path_to_results_scan, path_to_sheets_txt, evaluation_name, *args):
    separate_pdf_pages(path_to_original_scans, path_to_results_scan, evaluation_name)
    save_qr_data_to_file(path_to_sheets_txt, evaluation_name)

    path_to_sheets_txt = os.path.abspath(path_to_sheets_txt)
    QR_PATH = '{}/{}/{}_qr.txt'.format(path_to_sheets_txt, evaluation_name, evaluation_name)
    path_to_sheets_txt = f'{path_to_sheets_txt}/{evaluation_name}/{STUDENTS_FILE_TXT_NAME}'
    classify_tests_with_qr(path_to_sheets_txt, QR_PATH, path_to_results_scan)

if __name__ == '__main__':
    path1 = 'original_scans'
    path2 = 'scans'
    path3 = 'test_v1/i2/'
    ev = 'i2'
    classify_tests(path1, path2, path3, ev)