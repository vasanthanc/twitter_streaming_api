import argparse

'''
this class holds the argument parser functionality
in this way we can add options in ftr.
'''


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser ()

    '''
    this is a validation method, checking the
    value is empty.
    '''

    def check_string_and_not_expty(self, value):
        if not value.strip ():
            self.parser.print_help ()
            raise argparse.ArgumentTypeError ("empty string is invalid" % value)
        return value

    '''
    this method has options
    '''

    def parse_args(self, argv=None):
        self.parser.add_argument ('-q', '--query', type=self.check_string_and_not_expty, help='please pass the keyword')
        return self.parser.parse_args (argv)

# if __name__ == "__main__":
#     a = ArgumentParser()
#     print(a)
#     args = a.parse_args()
#     # a.check_string_and_not_expty(args.query)
#     # print(args.query)
