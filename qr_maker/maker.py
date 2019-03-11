import qrcode
from PIL import Image
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.log import print_progress_bar

QR_SAVE_PATH = f'{os.getcwd()}/QR'

def png_template_exists(path: str) -> bool:
    return not os.path.exists(f'{path}.png') and os.path.exists(f'{path}.pdf')

def new_qr(data: str, save=False) -> Image:
    _qr = qrcode.QRCode(version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=15, border=1)
    _qr.add_data(data)
    _qr.make(fit=True)
    _img = _qr.make_image(fill_color="black", back_color="white")

    save_img(_img, data) if save else None

    return _img

def make_qrs(_file_data: dict, _save_qr=False) -> list:
    _qrs_set = list()
    _lower_bound = int(_file_data['lower_bound'])
    _upper_bound = int(_file_data['upper_bound'])
    _course = _file_data['course']
    _eval = _file_data['evaluation']
    _template_path = _file_data['template']

    print_progress_bar(0, _upper_bound, prefix='\nProgress:', suffix='Complete', length=50)
    for idx in range(_lower_bound, _upper_bound + 1):
        _data = f'{_course}_{_eval}_{idx}'
        _qr_img = new_qr(_data, _save_qr)
        _template = Image.open(_template_path)
        _qrs_set.append((_qr_img, _template, _data))
        print_progress_bar(idx, _upper_bound, prefix='Progress:', suffix='Complete', length=50)

    return _qrs_set
    

def save_img(img: Image, data: str) -> None:

    os.mkdir(QR_SAVE_PATH) if not os.path.isdir(QR_SAVE_PATH) else None

    img.save(f'{data}.png')

if __name__ == '__main__':
    make_qr('iic2233/i1')

