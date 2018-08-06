import qrcode
import os

"""
To Do Version 1:
Get data from command line
"""

# Version 0
QR_DIRECTORY_PATH = './test'
def create_qrs(course, section, year, semester, evaluation_name, number):
    """
    Creates n *.png qr in format: course-section-year-semester-number and saves them in directory QR_DIRECTORY_PATH/evaluation_name/
    :param course: str that represents a UC course
    :param section: str that represents a UC course section
    :param year: str that represents the year of the course in format YYYY
    :param semester: str that represents either first or second semester (1 or 2)
    :param evaluation_name: str that represents test name (i1, i2, i3, exam)
    :param number: int that represents how many qr codes are needed
    :return None:
    """
    qr_string = "{}_"* 5 + "{}"
    # Creates directory if does not exist
    if not os.path.isdir("{}/{}".format(QR_DIRECTORY_PATH, evaluation_name)):
        os.mkdir("{}/{}".format(QR_DIRECTORY_PATH, evaluation_name))

    for num in range(1, number + 1):
        qr_data = qr_string.format(course, section, year, semester, evaluation_name, num)

        # Creates QR object
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Creates image from QR object
        img = qr.make_image(fill_color="black", back_color="white")
        path = "{}/{}/{}.png".format(QR_DIRECTORY_PATH, evaluation_name, qr_data)
        img.save(path)

if __name__ == '__main__':
    create_qrs('IIC2333','1','2018','2', 'i2', 1)