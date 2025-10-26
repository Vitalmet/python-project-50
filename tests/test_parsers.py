import pytest
import tempfile
import os
from gendiff.parsers import load_file, parse, get_format


def test_get_format():
    """Тест определения формата файла"""
    assert get_format('file.json') == 'json'
    assert get_format('file.yml') == 'yaml'
    assert get_format('file.yaml') == 'yaml'

    with pytest.raises(ValueError) as exc_info:
        get_format('file.txt')
    assert 'Unsupported file format' in str(exc_info.value)


def test_load_file_json():
    """Тест загрузки JSON файла"""
    # Создаем временный JSON файл
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{"key": "value"}')
        temp_file = f.name

    try:
        result = load_file(temp_file)
        assert result == {'key': 'value'}
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_load_file_yaml():
    """Тест загрузки YAML файла"""
    # Создаем временный YAML файл
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write('key: value')
        temp_file = f.name

    try:
        result = load_file(temp_file)
        assert result == {'key': 'value'}
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_parse_json():
    """Тест парсинга JSON данных"""
    result = parse('{"key": "value"}', 'json')
    assert result == {'key': 'value'}


def test_parse_yaml():
    """Тест парсинга YAML данных"""
    result = parse('key: value', 'yaml')
    assert result == {'key': 'value'}


def test_parse_unsupported_format():
    """Тест парсинга неподдерживаемого формата"""
    with pytest.raises(ValueError) as exc_info:
        parse('some content', 'xml')
    assert 'Unsupported format' in str(exc_info.value)


def test_parse_empty_content_json():
    """Тест парсинга пустого JSON содержимого"""
    # Пустой JSON должен вызывать ошибку
    with pytest.raises(ValueError):
        parse('', 'json')


def test_parse_empty_content_yaml():
    """Тест парсинга пустого YAML содержимого"""
    # Пустой YAML возвращает None
    result_yaml = parse('', 'yaml')
    assert result_yaml is None


def test_parse_whitespace_content_json():
    """Тест парсинга JSON содержимого только с пробелами"""
    # JSON с пробелами должен вызывать ошибку
    with pytest.raises(ValueError):
        parse('   ', 'json')


def test_parse_whitespace_content_yaml():
    """Тест парсинга YAML содержимого только с пробелами"""
    # YAML с пробелами возвращает None
    result_yaml = parse('   ', 'yaml')
    assert result_yaml is None


def test_parse_none_content_json():
    """Тест парсинга None JSON содержимого"""
    result_json = parse('null', 'json')
    assert result_json is None


def test_parse_none_content_yaml():
    """Тест парсинга None YAML содержимого"""
    result_yaml = parse('null', 'yaml')
    assert result_yaml is None


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


def test_load_file_nonexistent():
    """Тест загрузки несуществующего файла"""
    with pytest.raises(FileNotFoundError):
        load_file('nonexistent.json')