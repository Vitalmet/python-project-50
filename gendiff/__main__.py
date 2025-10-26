import argparse
import os
import sys
from gendiff.gendiff import generate_diff


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.',
        prog='gendiff'
    )

    parser.add_argument('first_file', help='first file to compare')
    parser.add_argument('second_file', help='second file to compare')

    parser.add_argument(
        '-f', '--format',
        metavar='FORMAT',
        default='stylish',
        choices=['stylish', 'plain', 'json'],
        help='output format (default: "stylish")'
    )

    parser.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s 1.0'
    )

    args = parser.parse_args()

    # Проверка существования файлов
    if not os.path.exists(args.first_file):
        print(f"Error: File '{args.first_file}' not found", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.second_file):
        print(f"Error: File '{args.second_file}' not found", file=sys.stderr)
        sys.exit(1)

    try:
        diff = generate_diff(args.first_file, args.second_file, args.format)
        print(diff)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
