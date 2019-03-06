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
        self.assertIsNone()

    def test_setup_option(self):
        pass
    
    def test_make_option(self):
        pass
    
    def test_classify_option(self):
        pass

    def tearDown(self):
        del self.parser

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CommandLineParseTest)
    unittest.TextTestRunner().run(suite)