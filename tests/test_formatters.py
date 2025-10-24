import os
from gendiff.scripts.diff_builder import build_diff
from gendiff.scripts.formatters.stylish import render
from gendiff.scripts.parsers import load_file


def test_render_stylish():
    """Тест рендеринга stylish формата"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    # Загружаем данные из файлов
    data1 = load_file(file1)
    data2 = load_file(file2)

    # Передаем данные, а не пути к файлам
    diff = build_diff(data1, data2)
    result = render(diff)

    assert isinstance(result, str)
    assert 'common' in result
    assert 'follow' in result


def test_render_stylish_empty():
    """Тест рендеринга пустого diff"""
    result = render({})
    assert result == '{\n}'


def test_render_stylish_nested():
    """Тест рендеринга вложенных структур"""
    diff = {
        'key': {
            'type': 'nested',
            'children': {
                'nested_key': {
                    'type': 'unchanged',
                    'value': 'nested_value'
                }
            }
        }
    }
    result = render(diff)
    assert 'key' in result
    assert 'nested_key' in result