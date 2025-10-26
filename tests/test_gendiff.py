import pytest
import os
from gendiff.gendiff import generate_diff


# Удалите несуществующий импорт parse_data


def test_identical_files():
    """Тест сравнения идентичных файлов"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    result = generate_diff(file1, file1)
    assert isinstance(result, str)
    assert 'common' in result


def test_different_files():
    """Тест сравнения разных файлов"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')
    result = generate_diff(file1, file2)
    assert isinstance(result, str)
    assert 'common' in result


def test_generate_diff_with_format():
    """Тест generate_diff с явным указанием формата"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    result_stylish = generate_diff(file1, file2, 'stylish')
    assert isinstance(result_stylish, str)
    assert 'common' in result_stylish


def test_generate_diff_invalid_format():
    """Тест generate_diff с неверным форматом"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    with pytest.raises(ValueError) as exc_info:
        generate_diff(file1, file2, 'invalid_format')
    assert 'Unsupported format' in str(exc_info.value)