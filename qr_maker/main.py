import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.log import cool_print_decoration, cool_print, print_invalid_file
from utils.file_merger import pdf_merger
from utils.file_converter import pdf_to_png
from utils.json_reader import check_file, read_data
from utils import create_directory

from .maker import make_qrs, png_template_exists
from .img_handler import composite_multiple_images

from PIL import Image

TEMPLATE_DIRECTORY = 'TEMPLATES'

def main(_file: str) -> int:

    _data = read_data(_file) if check_file(_file) else {}
    
    if not _data:
        print_invalid_file(_file)
        return 0
    
    COURSE_NAME = _data['course']
    EVALUATION = _data['evaluation']

    create_directory(f'{os.getcwd()}/ANSWER_SHEETS/') if not os.path.exists(f'{os.getcwd()}/ANSWER_SHEETS/') else None

    ANSWER_SHEETS_DIR_PATH = f'{os.getcwd()}/ANSWER_SHEETS/{COURSE_NAME}_{EVALUATION}'

    cool_print(f'\nAnswer sheets will be available in: {ANSWER_SHEETS_DIR_PATH}', style='result')

    cool_print(f'\n\nInitializing program...', style='info')
    
    if png_template_exists(f'{TEMPLATE_DIRECTORY}/{_data["template"]}'):
        cool_print_decoration('ERROR: Found template in .pdf format.\nConverting template to .png format...', 'danger')
        pdf_to_png(f'{TEMPLATE_DIRECTORY}/{_data["template"]}.pdf')

    create_directory(ANSWER_SHEETS_DIR_PATH) if not os.path.exists(ANSWER_SHEETS_DIR_PATH) else None

    _data['template'] = f'{TEMPLATE_DIRECTORY}/{_data["template"]}.png'
    cool_print(f'\nCreating QRs...', style='info')
    _qrs = make_qrs(_data, _save_qr=False)

    cool_print(f'\nPasting QRs in template...', style='info')
    _answer_sheets = composite_multiple_images(_qrs, _save_pages=False, _save_path=ANSWER_SHEETS_DIR_PATH)
    
    cool_print(f'\nMerging files...', style='info')
    pdf_merger(_answer_sheets, f'{ANSWER_SHEETS_DIR_PATH}/compilation.pdf')

    cool_print(f'\nDone!', style='info')

    return 1


if __name__ == '__main__':
    main()