import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows difference.',
        prog='gendiff'
)
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f', '--format',
        default='stylish',
        help='set format of output',
        metavar='FORMAT'
    )
    args = parser.parse_args()


if __name__ == '__main__':
    main()