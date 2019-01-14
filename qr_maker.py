import qrcode
import os
import sys
from log import cool_print_decoration
import argparse
from json import load
from generateQr.convert_files import add_qr_to_pdf
from wand.image import Image
from PyPDF2 import PdfFileMerger, PdfFileReader

# Version 0
QR_DIRECTORY_PATH = '{}/QR'.format(os.path.abspath(os.getcwd()));
PDF_FILE_PATH = '{}'.format(os.path.abspath('Plantilla.pdf'))
PAGES_PER_STUDENT = 1

def get_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = load(file)
    return data

def check_data_in_file(data_dict):
    for key in data_dict:
        if key in ['course', 'section', 'year', 'semester', 'evaluation', 'number'] and data_dict[key] == '':
            return False
    return True

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--course", action="store", dest="course_name", help="Course name: Ex. IIC2333")
    parser.add_argument('-s' ,"--section", action="store", dest="section_number", help="Section number: Ex. 7")
    parser.add_argument('-yy', "--year", action="store", dest="year_number", help="Year of course: Ex. 2018")
    parser.add_argument('-sem', "--semester", action="store", dest="semester_number", help="Semester number: 1 or 2")
    parser.add_argument('-e', "--evaluation", action="store", dest="evaluation_name", help="Evaluation name: i1, i2, i3, exam")
    parser.add_argument('-n', "--number", action="store", dest="number_qr",help="Numbers of correlated qr: Ex. 10")
    parser.add_argument('-f', "--file", action="store", dest="file_data",help="File where data is stored in JSON format")
    return parser.parse_args()

def create_qrs(course, section, year, semester, evaluation_name, lower_bound = 0 , number = 0, *args, **kwargs):
    """
    Creates n *.png qr in format: course-section-year-semester-number and saves them in directory QR_DIRECTORY_PATH/evaluation_name/
    :param course: str that represents a UC course
    :param section: str that represents a UC course section
    :param year: str that represents the year of the course in format YYYY
    :param semester: str that represents either first or second semester (1 or 2)
    :param evaluation_name: str that represents test name (i1, i2, i3, exam)
    :param number: int that represents how many qr codes are needed
    :return None:
    """

    paths_array = []

    qr_string = "{}_"* 2 + "{}"
    qr_path = "{}/{}/{}".format(QR_DIRECTORY_PATH, evaluation_name, course)
    # Creates directory if does not exist
    if not os.path.isdir(qr_path):
        os.makedirs(qr_path)

    image = Image(filename=PDF_FILE_PATH, resolution=400)
    for num in range(lower_bound, number + 1):
        qr_data = qr_string.format(course, section, num)

        # Creates QR object
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=15, border=1)
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Creates image from QR object
        img = qr.make_image(fill_color="black", back_color="transparent")
        path = "{}/{}/{}/{}.png".format(QR_DIRECTORY_PATH, evaluation_name, course ,qr_data)
        img.save(path)
        paths_array.append([path, PDF_FILE_PATH, path.split('.')[0] + '.pdf', num])
        
    list(map(lambda x: add_qr_to_pdf(*x, image), paths_array))
    compress_qrs(qr_path, evaluation_name, course)

def compress_qrs(qr_path = '', evaluation='', course = ''):
    files = [f for f in os.listdir(qr_path) if '.DS_' not in f]
    for _tuple in enumerate(sorted(files, key=lambda x: int(x.split('_')[-1][:-4]))) :
        index, file = _tuple
        file_path = os.path.abspath('{0}/{1}/{2}/{3}'.format('QR', evaluation, course ,file))
        print(file_path)
        output_pdf = PdfFileMerger()
        with open(file_path, 'rb') as pdf_file:
            input_pdf = PdfFileReader(pdf_file)
            for page_n in range(PAGES_PER_STUDENT):
                output_pdf.append(input_pdf)
            # output_pdf.append(input_pdf)
            # output_pdf.append(input_pdf)
            # output_pdf.append(input_pdf)
            # output_pdf.append(input_pdf)
        output_path = f"{qr_path}/compilado_{evaluation}_{index + 1}.pdf"
        with open(output_path, "wb") as output_stream:
            output_pdf.write(output_stream)


def main():
    arguments = parse_arguments()
    if arguments.file_data and not (arguments.course_name and arguments.section_number and arguments.year_number and
        arguments.semester_number and arguments.evaluation_name and arguments.number_qr):
        data = get_data_from_file(arguments.file_data)
        if not(check_data_in_file(data)):
            error_message = "Invalid arguments in file: {}. Please check file.".format(arguments.file_data)
            cool_print_decoration(error_message, style='alert')
        elif not os.path.exists(QR_DIRECTORY_PATH):
            error_message = "Invalid QR DIRECTORY PATH: {}".format(QR_DIRECTORY_PATH)
            cool_print_decoration(error_message, style = 'alert')
        else:
            data = [ data['course'], data['section'], data['year'], data['semester'], data['evaluation'], int(data['lower_bound']), int(data['number']) ]
            create_qrs(*data)
    elif not (arguments.course_name and arguments.section_number and arguments.year_number and
        arguments.semester_number and arguments.evaluation_name and arguments.number_qr and arguments.file_data):
        error_message = "Invalid arguments. Missing either --course, --section or --year or --semester or --evaluation_name or --number or --file."
        cool_print_decoration(error_message, style = 'alert')
    else:
        create_qrs(arguments.course_name, arguments.section_number, arguments.year_number,
        arguments.semester_number, arguments.evaluation_name, int(arguments.number_qr))

if __name__ == '__main__':
    # create_qrs('IIC2333','1','2018','2', 'i2', 1)
    main()
    # compress_qrs('./QR/C1')