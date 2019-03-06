import unittest
import os
import sys
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import utils.parse_arguments as p

class CommandLineParseTest(unittest.TestCase):
    
    def setUp(self):
        _parser = argparse.ArgumentParser()
        self.parser = p.create_arguments_main(_parser)
    
    def test_with_empty_args(self):
        _args = self.parser.parse_args([])
        self.assertEqual(p.check_option(_args), 0)

    def test_setup_option(self):
        _args = self.parser.parse_args(['-s'])
        self.assertEqual(p.check_option(_args), 1)
    
    def test_make_option(self):
        _args = self.parser.parse_args(['-f', 'qr_data.txt', '-m'])
        self.assertEqual(p.check_option(_args), 2)

    def test_classify_option(self):
        _args = self.parser.parse_args(['-f', 'qr_data.txt', '-c'])
        self.assertEqual(p.check_option(_args), 3)
    
    def test_all_flags(self):
        _args = self.parser.parse_args(['-m','-s', '-f', 'qr_data.txt', '-c'])
        self.assertEqual(p.check_option(_args), 1)

    def tearDown(self):
        del self.parser

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CommandLineParseTest)
    unittest.TextTestRunner().run(suite)