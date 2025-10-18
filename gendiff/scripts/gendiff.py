import argparse

import json


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

    with open(args.first_file) as f1, open(args.second_file) as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)


if __name__ == '__main__':
    main()