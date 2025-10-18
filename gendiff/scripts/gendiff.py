import argparse


def generate_diff(file_1, file_2,format_name='stylish'):
    return f"Comparing {file_1} and {file_2} in {format_name} format"


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

    diff = generate_diff(args.first_file, args.second_file, args.format)

    print(diff)


if __name__ == '__main__':
    main()