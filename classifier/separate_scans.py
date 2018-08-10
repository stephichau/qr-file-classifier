# from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
from wand.image import Image
from wand.color import Color
from cool_prints import cool_print_decoration, cool_print

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
    path = "{}/{}".format(result_separation_scans, evaluation_name)
    if not os.path.exists(path):
        cool_print_decoration('Making {} directory in path: {}'.format(evaluation_name, result_separation_scans), style = 'info')
        os.mkdir(path)

    original_scans_path = '{}/{}'.format(os.path.abspath(original_scans_path), evaluation_name)
    for question_file in os.listdir(original_scans_path):
        if not os.path.exists("{}/{}/".format(path, question_file.split('.')[0])):
            cool_print_decoration('Making {} directory in path: {}'.format(question_file.split('.')[0], result_separation_scans), style = 'info')
            os.mkdir("{}/{}".format(path, question_file.split('.')[0]))
        
        p = '{}/{}'.format(original_scans_path, question_file)
        input_pdf = PdfFileReader(open(p, "rb"))

        for i in range(input_pdf.numPages):
            output = PdfFileWriter()
            output.addPage(input_pdf.getPage(i))
            with open("{}/{}/{}.pdf".format(path, question_file.split('.')[0], i), "wb") as output_stream:
                output.write(output_stream)
                cool_print('Wrote in {}'.format("{}/{}/{}.pdf".format(path, question_file.split('.')[0], i)), style = 'result')
                file_path = "{}/{}/{}.pdf".format(path, question_file.split('.')[0], i)
                # convert_pdf_to_png(file_path)
                cool_print('Converted in {}'.format("{}/{}/{}.pdf".format(path, question_file.split('.')[0], i)), style = 'info')

def convert_pdf_to_png(file):
    with wImage(filename=file) as img:
        print(img)
        # with wImage(width=img.width, height=img.height, background=cColor("white")) as bg:
            #bg.composite(img,0,0)
            #bg.save(filename="{}.png".format(file))

if __name__ == '__main__':
    path1 = 'original_scans'
    path2 = 'scans'
    # separate_pdf_pages(path1, path2, 'i1')

    # imageDir = r'____' # your imagedirectory path
    # SaveToDir = r'____' # diretory in which you want to save the pdfs
    # makePdf(imageDir, SaveToDir)
    m = os.path.abspath('classifier/0.pdf')
    print(m)
    # with Image(filename=m) as img:
    #    img.save(filename="temp.jpg")
    all_pages = Image(blob='classifier/0.pdf')        # PDF will have several pages.
    """ single_image = all_pages.sequence[0]    # Just work on first page
    with Image(single_image) as i:
        i.format = 'png'
        i.background_color = Color('white') # Set white background.
        i.alpha_channel = 'remove' """