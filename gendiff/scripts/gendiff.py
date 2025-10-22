import argparse
import os
from .parser import load_file


def format_value(value):
    if value is True:
        return 'true'
    elif value is False:
        return 'false'
    elif value is None:
        return 'null'
    else:
        return str(value)


def generate_diff(file_path1, file_path2):
    # Загружаем данные через парсер
    data1 = load_file(file_path1)
    data2 = load_file(file_path2)

    result = []
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))

    for key in all_keys:
        if key not in data1:
            result.append(f"  + {key}: {format_value(data2[key])}")
        elif key not in data2:
            result.append(f"  - {key}: {format_value(data1[key])}")
        else:
            if data1[key] != data2[key]:
                result.append(f"  - {key}: {format_value(data1[key])}")
                result.append(f"  + {key}: {format_value(data2[key])}")
            else:
                result.append(f"    {key}: {format_value(data1[key])}")

    return "{\n" + "\n".join(result) + "\n}"


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
        help='set format of output',
        metavar='FORMAT'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0'
    )

    args = parser.parse_args()

    # Если не указаны оба файла, показываем справку
    if args.first_file is None or args.second_file is None:
        parser.print_help()
        return

    # Проверяем существование файлов
    if not os.path.exists(args.first_file):
        print(f"Error: File '{args.first_file}' not found")
        return 1

    if not os.path.exists(args.second_file):
        print(f"Error: File '{args.second_file}' not found")
        return 1

    diff_str = generate_diff(args.first_file, args.second_file)
    print(diff_str)


if __name__ == '__main__':
    main()