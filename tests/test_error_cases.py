import pytest
import os
import tempfile
import yaml
from gendiff.scripts.gendiff import generate_diff
from gendiff.scripts.parsers import load_file

def test_generate_diff_nonexistent_file():
    """Тест с несуществующим файлом"""
    with pytest.raises(FileNotFoundError):
        generate_diff('nonexistent1.json', 'nonexistent2.json')


def test_generate_diff_invalid_json():
    """Тест с некорректным JSON файлом"""
    # Создаем временный файл с некорректным JSON
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('invalid json content')
        temp_file = f.name

    try:
        with pytest.raises(ValueError):
            generate_diff(temp_file, 'tests/fixtures/file1.json')
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_generate_diff_invalid_yaml():
    """Тест с некорректным YAML файлом"""
    # Создаем временный файл с действительно некорректным YAML
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write('invalid: [yaml: content}')  # более явно некорректный YAML
        temp_file = f.name

    try:
        with pytest.raises((ValueError, yaml.scanner.ScannerError, yaml.parser.ParserError)):
            generate_diff(temp_file, 'tests/fixtures/file1.json')
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_load_file_unsupported_format():
    """Тест загрузки файла с неподдерживаемым форматом"""
    # Создаем временный файл с неподдерживаемым расширением
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('some content')
        temp_file = f.name

    try:
        with pytest.raises(ValueError) as exc_info:
            load_file(temp_file)
        assert 'Unsupported file format' in str(exc_info.value)
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_generate_diff_empty_files():
    """Тест сравнения пустых файлов"""
    # Создаем временные пустые файлы
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        f1.write('{}')
        temp_file1 = f1.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        f2.write('{}')
        temp_file2 = f2.name

    try:
        result = generate_diff(temp_file1, temp_file2)
        assert isinstance(result, str)
        assert result == '{\n}'
    finally:
        # Удаляем временные файлы
        if os.path.exists(temp_file1):
            os.remove(temp_file1)
        if os.path.exists(temp_file2):
            os.remove(temp_file2)