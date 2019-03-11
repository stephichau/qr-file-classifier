import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import qr_maker.maker as qr

class QrMakerTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_template_checker_pdf(self):
        pass

    def test_merger(self):
        pass
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(QrMakerTest)
    unittest.TextTestRunner().run(suite)