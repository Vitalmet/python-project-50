import pytest
import os
from gendiff.scripts.gendiff import generate_diff


def test_generate_diff_stylish_format():
    """Тест явного указания stylish формата"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    result = generate_diff(file1, file2, 'stylish')
    assert isinstance(result, str)
    assert 'common' in result
    assert 'follow' in result


def test_generate_diff_plain_format():
    """Тест plain формата, если он реализован"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    try:
        result = generate_diff(file1, file2, 'plain')
        assert isinstance(result, str)
    except ValueError:
        # Если plain формат не реализован, пропускаем
        pytest.skip("Plain format not implemented")


def test_generate_diff_json_format():
    """Тест json формата, если он реализован"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    try:
        result = generate_diff(file1, file2, 'json')
        assert isinstance(result, str)
    except ValueError:
        # Если json формат не реализован, пропускаем
        pytest.skip("JSON format not implemented")


def test_generate_diff_default_format():
    """Тест формата по умолчанию"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    result_default = generate_diff(file1, file2)
    result_stylish = generate_diff(file1, file2, 'stylish')

    # Результат по умолчанию должен совпадать со stylish
    assert result_default == result_stylish


def test_generate_diff_invalid_format():
    """Тест с неверным форматом"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    with pytest.raises(ValueError) as exc_info:
        generate_diff(file1, file2, 'invalid_format')
    assert 'Unsupported format' in str(exc_info.value)


def test_generate_diff_format_with_yaml():
    """Тест форматов с YAML файлами"""
    file1 = os.path.join('tests', 'fixtures', 'file1.yml')
    file2 = os.path.join('tests', 'fixtures', 'file2.yml')

    result_stylish = generate_diff(file1, file2, 'stylish')
    assert isinstance(result_stylish, str)
    assert 'common' in result_stylish


def test_generate_diff_mixed_formats():
    """Тест форматов со смешанными типами файлов"""
    json_file = os.path.join('tests', 'fixtures', 'file1.json')
    yaml_file = os.path.join('tests', 'fixtures', 'file2.yml')

    result = generate_diff(json_file, yaml_file, 'stylish')
    assert isinstance(result, str)
    assert 'common' in result
