from wand.image import Image
from wand.color import Color

def pdf_to_png(f_name: str) -> None:
    image = Image(filename=f_name, resolution=300)
    with Image(image) as i:
        i.format = 'png'
        i.background_color = Color('white')
        i.alpha_channel = 'remove'
        i.save(filename=f_name.replace('pdf', 'png'))