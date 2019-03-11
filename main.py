from testing.setup import *
from sys import argv
import utils.parse_arguments as p
from utils.json_reader import read_data
from utils.log import cool_print_decoration
from argparse import ArgumentParser
from qr_maker import main as make

OPTIONS = { # To Do: Change strings for callables
    1: 'Setup test',
    2: make.main,
    3: 'Classify'
}

def main():
    _parser = ArgumentParser()
    _args = p.create_arguments_main(_parser).parse_args(argv[1:])
    _opt = p.check_option(_args)
    
    OPTIONS[_opt]() if _opt == 1 else None
    OPTIONS[_opt](_args.filename) if _opt > 1 else print_invalid_options()
    

def print_invalid_options():
    _msg = 'Invalid commands from CLI.\nPlease check available flags'
    cool_print_decoration(_msg, 'danger')

if __name__ == '__main__':
    main()