import argparse

def create_arguments_main(parser: argparse.ArgumentParser) -> argparse.Namespace:
    parser.add_argument('-s', "--setup", action="store_true", dest="setup", help="Setup mode")
    parser.add_argument('-m' ,"--make", action="store_true", dest="make", help="Create qr")
    parser.add_argument('-f' ,"--file", action="store", dest="filename",
        help="Info either for creating QR's or classifying")
    parser.add_argument('-c' ,"--classify", action="store_true", dest="classify", help="Create qr")
    # parser.add_argument('-yy', "--year", action="store", dest="year_number", help="Year of course: Ex. 2018")
    # parser.add_argument('-sem', "--semester", action="store", dest="semester_number", help="Semester number: 1 or 2")
    # parser.add_argument('-e', "--evaluation", action="store", dest="evaluation_name", help="Evaluation name: i1, i2, i3, exam")
    # parser.add_argument('-n', "--number", action="store", dest="number_qr",help="Numbers of correlated qr: Ex. 10")
    # parser.add_argument('-f', "--file", action="store", dest="file_data",help="File where data is stored in JSON format")
    # return parser.parse_args()
    return parser

def check_option(arguments: argparse.Namespace) -> int: # rename function
    option = 0

    option = 1 if check_setup(arguments) else option

    option = 2 if option == 0 and check_qr_make(arguments) else option

    option = 3 if option == 0 and check_qr_classify(arguments) else option

    return option
    
def check_setup(arguments: argparse.Namespace) -> bool:
    return arguments and arguments.setup

def check_qr_make(arguments: argparse.Namespace) -> bool:
    return arguments and arguments.make and arguments.filename and not arguments.classify

def check_qr_classify(arguments: argparse.Namespace) -> bool:
    return arguments and arguments.classify and arguments.filename and not arguments.make


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    p = create_arguments_main(parser)
    print(chosen_option(p))