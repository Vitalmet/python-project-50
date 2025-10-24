import pytest
import os
from gendiff.scripts.gendiff import generate_diff


def test_generate_diff_complete_workflow():
    """Полный тест workflow generate_diff"""
    test_cases = [
        ('file1.json', 'file2.json', 'stylish'),
        ('file1.yml', 'file2.yml', 'stylish'),
        ('file1.json', 'file2.yml', 'stylish'),
    ]

    for file1_name, file2_name, format_name in test_cases:
        file1 = os.path.join('tests', 'fixtures', file1_name)
        file2 = os.path.join('tests', 'fixtures', file2_name)

        result = generate_diff(file1, file2, format_name)
        assert isinstance(result, str)
        assert len(result) > 0


def test_generate_diff_with_nonexistent_format():
    """Тест с несуществующим форматом вывода"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    with pytest.raises(ValueError) as exc_info:
        generate_diff(file1, file2, 'nonexistent_format')

    assert 'Unsupported format' in str(exc_info.value)


def test_generate_diff_build_diff_integration():
    """Интеграционный тест build_diff внутри generate_diff"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    result = generate_diff(file1, file2, 'stylish')

    assert 'common' in result
    assert 'follow' in result
    assert 'setting1' in result


def test_generate_diff_format_dispatch():
    """Тест диспетчеризации форматов в generate_diff"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    supported_formats = ['stylish']

    for format_name in supported_formats:
        result = generate_diff(file1, file2, format_name)
        assert isinstance(result, str)
        assert 'common' in result


def test_generate_diff_empty_result():
    """Тест случая когда diff пустой"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')

    result = generate_diff(file1, file1, 'stylish')
    assert isinstance(result, str)
