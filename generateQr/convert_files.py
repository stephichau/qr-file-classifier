import os
from wand.image import Image
from wand.display import display
from log import cool_print

"""
Solution based from
https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images
"""

QR_POSITION_PONDERATOR = 1.6

def add_qr_to_pdf(qr_file_path, pdf_file_path, output_path, image = None,*args, **kwargs):
    """
    Adds qr to .pdf and saves .pdf
    """
    full_path = "{}".format(pdf_file_path)
    with Image(image=image) as img:
        # img.strip()
        # img.save(filename=output_path)
        with Image(filename=qr_file_path, resolution=300) as qr:
            qr.resize(int(qr.width*0.7), int(qr.height* 0.7))
            left = int(img.width - qr.width * QR_POSITION_PONDERATOR)
            top = 60
            img.composite(qr, left=left, top=top)
        img.save(filename=output_path)
        os.remove(qr_file_path)
        # cool_print('Converted in {}'.format("{}".format(output_path)), style = 'result')
    # qr = os.path.abspath('QR/i1/IIC2233_1_2018_2_i1_1.png')
    # add_qr_image(qr_file_path, output_path)


def compile_data(qr_directory_path, evaluation_name, *args, **kwargs):
    compiled_pdf_path = f'{qr_directory_path}/{evaluation_name}/{evaluation_name}.pdf'

if __name__ == '__main__':
    p = os.path.abspath('Plantilla.pdf')
    o = os.path.abspath('TestsQr') + '/test.png'
    qr = os.path.abspath('QR/i1/IIC2233_1_2018_2_i1_1.png')
    print(p)
    convert_pdf_to_png(qr, p, o)