import argparse

def main():
    parser = argparse.ArgumentParser(
        description='Compare files and show differences'
)
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', default='stylish')
    args = parser.parse_args()

    print(f"Comparing {args.first_file} and {args.second_file} in {args.format} format")
if __name__ == '__main__':
    main()