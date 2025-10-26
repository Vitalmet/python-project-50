import json
import tempfile
import pytest
from gendiff.gendiff import generate_diff

# Условный импорт для YAML
try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def create_test_file(data, extension='.json'):
    """Создает временный файл с данными в указанном формате"""
    fd, path = tempfile.mkstemp(suffix=extension)
    with open(fd, 'w') as f:
        if extension in ['.yml', '.yaml'] and YAML_AVAILABLE:
            yaml.dump(data, f)
        else:
            json.dump(data, f)
    return path


class TestGendiff:
    """Минимальные тесты для gendiff"""

    def test_json_comparison(self):
        """Сравнение JSON файлов - основной сценарий"""
        file1 = create_test_file({
            "host": "hexlet.io",
            "timeout": 50,
            "proxy": "123.234.53.22",
            "follow": False
        }, '.json')
        file2 = create_test_file({
            "timeout": 20,
            "verbose": True,
            "host": "hexlet.io"
        }, '.json')

        result = generate_diff(file1, file2)

        expected = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
        assert result == expected

    def test_yaml_comparison(self):
        """Сравнение YAML файлов - основной сценарий"""
        if not YAML_AVAILABLE:
            pytest.skip("PyYAML not available")

        file1 = create_test_file({
            "host": "hexlet.io",
            "timeout": 50,
            "proxy": "123.234.53.22",
            "follow": False
        }, '.yml')
        file2 = create_test_file({
            "timeout": 20,
            "verbose": True,
            "host": "hexlet.io"
        }, '.yml')

        result = generate_diff(file1, file2)

        expected = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
        assert result == expected