from PIL import Image, ImageDraw, ImageFont
from pyzbar.pyzbar import decode
import os
QR_RESULTS_DIRECTORY = './Results-{}-{}'
from wand.image import Image as wImage

"""
Based on code found in:
https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
https://github.com/NaturalHistoryMuseum/pyzbar/blob/master/bounding_box_and_polygon.py
"""

def save_data(image, qr_data):
    data_split = qr_data.split('_')
    output_directory = QR_RESULTS_DIRECTORY.format(data_split[0], data_split[-2])
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    output_path = "{}/{}.png".format(output_directory, qr_data.split('_')[-1])
    if not os.path.exists(output_path):
        image.save(output_path)

def find_and_decode_qr_from_image(path = None, image = None, *args, **kwargs):
    """
    :param path: Represents absolute path of image with qr
    :return qr_data: Represents data extracted from QR
    """
    if not image:
        image = Image.open(path).convert('RGB')
    # draw = ImageDraw.Draw(image)
    qr_data = ''
    for qr in decode(image):
        # rect = qr.rect
        # draw.rectangle(
        #    (
        #        (rect.left, rect.top),
        #        (rect.left + rect.width, rect.top + rect.height)
        #    ),
        #    outline='#ff0000'
        #)

        # draw.polygon(qr.polygon, outline='#e945ff')
        qr_data = qr.data.decode('utf-8')
    # This part is meant for testing
    """if (qr_data.count('_') > 2):
        save_data(image, qr_data)"""
    return qr_data

if __name__ == '__main__':
    # print(find_and_decode_qr_from_image('scans/i2/Back/0.png'))
    with wImage(filename='scans/i1/i1-p1/0.pdf') as img:
        print(find_and_decode_qr_from_image(image=img))