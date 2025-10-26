# gendiff/gendiff.py

from .parsers import load_file
from .diff_builder import build_diff
from .formatters.stylish import render as render_stylish
from .formatters.plain import render_plain
from .formatters.json import render_json


def generate_diff(file_path1, file_path2, format_name='stylish'):

    data1 = load_file(file_path1)
    data2 = load_file(file_path2)

    diff = build_diff(data1, data2)

    if format_name == 'stylish':
        return render_stylish(diff)
    elif format_name == 'plain':
        return render_plain(diff)
    elif format_name == 'json':
        return render_json(diff)
    else:
        raise ValueError(f"Unsupported format: {format_name}")