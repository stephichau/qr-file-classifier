import os

def pdf_merger(_img_list: list, _path_name: str) -> None:
    _img_list[0].save(_path_name, 'PDF', resolution=100,
        save_all=True, append_images=_img_list[1:])
