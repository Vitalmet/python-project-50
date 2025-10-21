import json
import tempfile
import pytest
import yaml
from gendiff.scripts.gendiff import generate_diff


def create_test_file(data, extension='.json'):
    """Создает временный файл с данными в указанном формате"""
    fd, path = tempfile.mkstemp(suffix=extension)
    with open(fd, 'w') as f:
        if extension in ['.yml', '.yaml']:
            yaml.dump(data, f)
        else:
            json.dump(data, f)
    return path


class TestGendiff:

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