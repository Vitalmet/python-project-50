import json
import argparse


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
    with open(file_path1) as f1:
        data1 = json.load(f1)

    with open(file_path2) as f2:
        data2 = json.load(f2)

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
    args = parser.parse_args()

    diff_str = generate_diff(args.first_file, args.second_file)
    print(diff_str)


if __name__ == '__main__':
    main()
