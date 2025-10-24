import argparse
import os
from .parsers import load_file
from .diff_builder import build_diff
from .formatters.stylish import render as render_stylish


def generate_diff(file_path1, file_path2, format_name='stylish'):
    """
    Генерирует различия между двумя файлами
    """
    data1 = load_file(file_path1)
    data2 = load_file(file_path2)

    diff = build_diff(data1, data2)

    if format_name == 'stylish':
        return render_stylish(diff)
    else:
        raise ValueError(f"Unsupported format: {format_name}")


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.',
        prog='gendiff',
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f', '--format',
        default='stylish',
        help='set format of output (default: stylish)',
        metavar='FORMAT'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0'
    )

    args = parser.parse_args()

    if args.first_file is None or args.second_file is None:
        parser.print_help()
        return

    if not os.path.exists(args.first_file):
        print(f"Error: File '{args.first_file}' not found")
        return 1

    if not os.path.exists(args.second_file):
        print(f"Error: File '{args.second_file}' not found")
        return 1

    diff_str = generate_diff(args.first_file, args.second_file, args.format)
    print(diff_str)


if __name__ == '__main__':
    main()