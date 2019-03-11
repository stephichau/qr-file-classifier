from PIL import Image

QR_POSITION_PONDERATOR = 1.65

def composite_img(_qr_img: Image, _template: Image, _data:str, _save_page=False, _save_path='') -> Image:
    # img.resize((int(img.width*0.6), int(img.height* 0.6)))
    _left = int(_template.width - _qr_img.width * QR_POSITION_PONDERATOR)
    _top = 110
    _template.paste(_qr_img, (int(_template.width * 0.9 - _qr_img.width), 0))

    _template.save(f'{_save_path}/{_data}.png') if _save_page else None

    return _template

def composite_multiple_images(_qrs: set, _save_pages=False, _save_path='') -> list:
    return list(map(lambda _img_tuple:
        composite_img(*_img_tuple, _save_page=_save_pages, _save_path=_save_path), _qrs))