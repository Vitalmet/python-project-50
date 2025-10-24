import json
import tempfile
from gendiff.scripts.gendiff import generate_diff


def create_test_file(data):
    """Создает временный JSON файл с данными"""
    fd, path = tempfile.mkstemp(suffix='.json')
    with open(fd, 'w') as f:
        json.dump(data, f)
    return path


def test_identical_files():
    """Тест одинаковых файлов"""
    data = {"name": "John", "age": 30}
    file1 = create_test_file(data)
    file2 = create_test_file(data)

    result = generate_diff(file1, file2)

    # Реальный вывод для одинаковых файлов
    expected = """{
    age: 30
    name: John
}"""
    assert result == expected


def test_different_files():
    """Тест разных файлов"""
    file1 = create_test_file({
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22",
        "follow": False
    })
    file2 = create_test_file({
        "timeout": 20,
        "verbose": True,
        "host": "hexlet.io"
    })

    result = generate_diff(file1, file2)

    # Реальный вывод для разных файлов
    expected = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
    assert result == expected


def test_added_key():
    """Тест добавления ключа"""
    file1 = create_test_file({"name": "John"})
    file2 = create_test_file({"name": "John", "age": 30})

    result = generate_diff(file1, file2)

    assert "+ age: 30" in result
    assert "name: John" in result


def test_removed_key():
    """Тест удаления ключа"""
    file1 = create_test_file({"name": "John", "age": 30})
    file2 = create_test_file({"name": "John"})

    result = generate_diff(file1, file2)

    assert "- age: 30" in result
    assert "name: John" in result


def test_changed_value():
    """Тест изменения значения"""
    file1 = create_test_file({"age": 30})
    file2 = create_test_file({"age": 25})

    result = generate_diff(file1, file2)

    assert "- age: 30" in result
    assert "+ age: 25" in result