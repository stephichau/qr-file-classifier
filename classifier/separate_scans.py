from PyPDF2 import PdfFileWriter, PdfFileReader
import os
from wand.image import Image
from wand.color import Color
from .cool_prints import cool_print_decoration, cool_print
from .decode_data import save_data, find_and_decode_qr_from_image
import json
import numpy as np
import cv2

QR_VALUE_FILE_PATHS_DICT = {}

def separate_pdf_pages(original_scans_path, result_separation_scans, evaluation_name, *args):
    """
    Separates multiple paged .pdf into multiple .pdf files
    """
    # Get abs path of directories
    original_scans_path = '{}/{}'.format(os.path.abspath(original_scans_path), evaluation_name)
    result_separation_scans = '{}/{}'.format(os.path.abspath(result_separation_scans), evaluation_name)

    if not os.path.exists(result_separation_scans):
        cool_print_decoration('Creating directory in path {}'.format(result_separation_scans), style = 'info')
        os.mkdir(result_separation_scans)
    
    list_dir = [f for f in os.listdir(original_scans_path) if not f.startswith('.DS_S')]

    # Scans are front and back (even number)
    for question_file in list_dir:

        # Get abs path of files and question_directories
        file_path = '{}/{}'.format(original_scans_path, question_file)
        question_directory = question_file.split('.')[0]
        result_question_path = '{}/{}'.format(result_separation_scans, question_directory)
        if not os.path.exists(result_question_path):
            os.mkdir(result_question_path)
        
        # Start separation
        with open(file_path, 'rb') as pdf_file:
            input_pdf = PdfFileReader(pdf_file)
            # Scans are from front and back
            for page_n in range(0, input_pdf.numPages):
                if page_n % 2 == 1:
                    continue
                output_path = '{}/{}_{}.pdf'.format(result_question_path, question_directory, page_n)
                output_path_back_page = '{}/{}_{}.pdf'.format(result_question_path, question_directory, page_n + 1)
                if not os.path.exists(output_path) or not os.path.exists(output_path_back_page):
                    output_pdf = PdfFileWriter()
                    output_pdf_back = PdfFileWriter()

                    output_pdf.addPage(input_pdf.getPage(page_n))
                    output_pdf_back.addPage(input_pdf.getPage(page_n + 1))

                    write_pdf(output_pdf, output_path)
                    write_pdf(output_pdf_back, output_path_back_page)

                convert_pdf_to_png(output_path, output_path_back_page)

def write_pdf(output_pdf, output_path):
    with open(output_path, "wb") as output_stream:
        output_pdf.write(output_stream)
        cool_print('Wrote in {}'.format(output_path), style = 'result')

def convert_pdf_to_png(file_path, back_page = None):
    """
    Converts .pdf to .png and stores it until qr is detected and key, value are stored in dictionary
    """
    full_path = "{}".format(file_path)
    # output_path = "{}.png".format(file_path.split('.')[0])
    output_path = "{}.png".format(file_path.split('.')[0])
    with Image(filename=full_path, resolution=500) as img:
        img.strip()
        # img.crop(int(img.width * 0.7), 0, img.width, int(img.height * 0.2))
        # img.crop(int(img.width * 0.8), 20, int(img.width * 0.95), int(img.height * 0.125))
        img.crop(int(img.width * 0.7), 0, int(img.width), int(img.height * 0.5))
        img.save(filename=output_path)

        cool_print('Converted in {}'.format("{}".format(output_path)), style = 'result')
        split_data_number = find_and_decode_qr_from_image(path = output_path)

        split_data_number = split_data_number.split('_')[-1]
        if not QR_VALUE_FILE_PATHS_DICT.get(split_data_number):
            QR_VALUE_FILE_PATHS_DICT[split_data_number] = []
        QR_VALUE_FILE_PATHS_DICT[split_data_number].append(file_path)
        QR_VALUE_FILE_PATHS_DICT[split_data_number].append(back_page)

        # Remove tmp file
        
        os.remove(output_path)
        cool_print('Removed file {}\n'.format("{}".format(output_path)), style = 'result')

def save_qr_data_to_file(path_to_sheets_txt, evaluation_name):
    path = '{}/{}/{}_qr.txt'.format(path_to_sheets_txt, evaluation_name, evaluation_name)
    with open(path, 'w') as file:
        json.dump(QR_VALUE_FILE_PATHS_DICT, file, indent=4)
    cool_print_decoration('Successfully wrote in {}'.format(path), style='result')

if __name__ == '__main__':
    path1 = 'original_scans'
    path2 = 'scans'
    separate_pdf_pages(path1, path2, 'i2')