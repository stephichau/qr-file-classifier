import os
from .decode_data import save_data, find_and_decode_qr_from_image

QR_ORIGINAL_TESTS_DIRECTORY = './test/'
# cambiar nombre a hojas escaneadas

def classify_tests():
    for ev in os.listdir(QR_ORIGINAL_TESTS_DIRECTORY):
        if os.path.isfile(ev):
            continue
        path2 = QR_ORIGINAL_TESTS_DIRECTORY + "{}/".format(ev)
        for file in os.listdir(path2):
            if file.startswith('.'):
                continue
            file_path = "{}/{}".format(os.path.abspath(path2), file)
            print(find_and_decode_qr_from_image(file_path))
        
if __name__ == '__main__':
    classify_tests()