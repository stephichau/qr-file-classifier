from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pyzbar.pyzbar import decode, ZBarSymbol
from wand.image import Image as WImage
import cv2
import os
import numpy as np
from .cool_prints import cool_print_decoration

QR_RESULTS_DIRECTORY = './Results-{}-{}'

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
        print("Saving in {}".format(output_path))
        image.save(output_path)

def find_and_decode_qr_from_image(path = None, image = None, *args, **kwargs):
    """
    :param path: Represents absolute path of image with qr
    :return qr_data: Represents data extracted from QR
    """
    kernel = np.ones((2,2),np.uint8)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    image = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    # image = cv2.erode(img, kernel, iterations = 1)
    # image = cv2.dilate(img, kernel, iterations=2)
    # if not image:
    #      image = Image.open(path).convert('RGB')
    # draw = ImageDraw.Draw(image)
    qr_data = ''
    for qr in decode(image, symbols=[ZBarSymbol.QRCODE]):
        # print(qr)
        qr_data = qr.data.decode('utf-8')
        cool_print_decoration('Decoding:\n{}'.format(qr_data), style='info')
    return qr_data

if __name__ == '__main__':
    pass
    # path = 'results/MT/midterm-p4/dalal.png'
    # print(path)
    # print(find_and_decode_qr_from_image(path))