# from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
from wand.image import Image
from wand.color import Color
from cool_prints import cool_print_decoration, cool_print
from decode_data import save_data, find_and_decode_qr_from_image

# Based from: https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images
def makePdf(imageDir, SaveToDir):
    '''
    imageDir: Directory of your images
    SaveToDir: Location Directory for your pdfs
    '''
    os.chdir(imageDir)
    try:
        for j in os.listdir(os.getcwd()):
            os.chdir(imageDir)
            fname, fext = os.path.splitext(j)
            newfilename = fname + ".pdf"
            im = Image.open(fname + fext)
            if im.mode == "RGBA":
                im = im.convert("RGB")
            os.chdir(SaveToDir)
            if not os.path.exists(newfilename):
                im.save(newfilename, "PDF", resolution=100.0)
    except Exception as e:
        print(e)

def separate_pdf_pages(original_scans_path, result_separation_scans, evaluation_name, *args):
    # Get abs path of directories
    original_scans_path = '{}/{}'.format(os.path.abspath(original_scans_path), evaluation_name)
    if not os.path.exists('{}/{}'.format(os.path.abspath(result_separation_scans), evaluation_name)):
        cool_print_decoration('Creating directory in path {}'.format('{}/{}'.format(os.path.abspath(result_separation_scans), evaluation_name)), style = 'info')
        os.mkdir('{}/{}'.format(os.path.abspath(result_separation_scans), evaluation_name))
    result_separation_scans = '{}/{}'.format(os.path.abspath(result_separation_scans), evaluation_name)

    for question_file in os.listdir(original_scans_path):
        # Get abs path of files and question_directories
        file_path = '{}/{}'.format(original_scans_path, question_file)
        filename = question_file.split('.')[0]
        if not os.path.exists('{}/{}'.format(result_separation_scans, filename)):
            os.mkdir('{}/{}'.format(result_separation_scans, filename))
        result_question_path = '{}/{}'.format(result_separation_scans, filename)

        # Start separation
        with open(file_path, 'rb') as pdf_file:
            input_pdf = PdfFileReader(pdf_file)
            for page_n in range(input_pdf.numPages):
                output_path = '{}/{}.pdf'.format(result_question_path, page_n)
                output_pdf = PdfFileWriter()
                output_pdf.addPage(input_pdf.getPage(page_n))
                write_pdf(output_pdf, output_path)
                convert_pdf_to_png(output_path)

def write_pdf(output_pdf, output_path):
    with open(output_path, "wb") as output_stream:
        output_pdf.write(output_stream)
        cool_print('Wrote in {}'.format(output_path), style = 'result')

def convert_pdf_to_png(file_path):
    full_path = "{}".format(file_path)
    output_path = "{}.png".format(file_path.split('.')[0])
    with Image(filename=full_path, resolution=300) as img:
        img.strip()
        img.crop(int(img.width * 0.6), 0, img.width, int(img.height * 0.2))
        img.save(filename=output_path)
    cool_print('Converted in {}\n'.format("{}".format(output_path)), style = 'result')

if __name__ == '__main__':
    path1 = 'original_scans'
    path2 = 'scans'
    separate_pdf_pages(path1, path2, 'i2')
    # imageDir = r'____' # your imagedirectory path
    # SaveToDir = r'____' # diretory in which you want to save the pdfs
    # makePdf(imageDir, SaveToDir)
    # m = os.path.abspath('scans/i1/i1-p1')
    # name = '0'
    # convert_pdf_to_png(m,name)
    # with Image(filename=m, resolution=300) as img:
    #    img.save(filename="temp.png")