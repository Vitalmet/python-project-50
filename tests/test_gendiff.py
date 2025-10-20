import os
import json
import tempfile
import pytest

# Убираем неиспользуемый импорт format_value
from gendiff.scripts.gendiff import generate_diff


class TestGenerateDiff:
    """Тесты для основной функции generate_diff"""

    @pytest.fixture
    def create_temp_files(self):
        """Фикстура для создания временных файлов"""
        files = []

        def _create_file(content):
            fd, path = tempfile.mkstemp(suffix='.json', dir=os.getcwd())
            with os.fdopen(fd, 'w') as f:
                if isinstance(content, dict):
                    json.dump(content, f)
                else:
                    f.write(content)
            files.append(path)
            return path

        yield _create_file

        # Очистка после тестов
        for file_path in files:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_identical_files(self, create_temp_files):
        """Тест одинаковых файлов"""
        data = {"name": "John", "age": 30, "city": "New York"}
        file1 = create_temp_files(data)
        file2 = create_temp_files(data)

        result = generate_diff(file1, file2)

        expected = """{
    age: 30
    city: New York
    name: John
}"""
        assert result == expected

    def test_specific_files_comparison(self, create_temp_files):
        """Тест сравнения конкретных файлов из задания"""
        file1 = create_temp_files({
            "host": "hexlet.io",
            "timeout": 50,
            "proxy": "123.234.53.22",
            "follow": False
        })
        file2 = create_temp_files({
            "timeout": 20,
            "verbose": True,
            "host": "hexlet.io"
        })

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

    def test_different_values(self, create_temp_files):
        """Тест файлов с разными значениями"""
        file1 = create_temp_files({"name": "John", "age": 30})
        file2 = create_temp_files({"name": "Jane", "age": 25})

        result = generate_diff(file1, file2)

        expected = """{
  - age: 30
  + age: 25
  - name: John
  + name: Jane
}"""
        assert result == expected

    def test_added_key(self, create_temp_files):
        """Тест добавления нового ключа"""
        file1 = create_temp_files({"name": "John"})
        file2 = create_temp_files({"name": "John", "age": 30})

        result = generate_diff(file1, file2)

        expected = """{
  + age: 30
    name: John
}"""
        assert result == expected

    def test_removed_key(self, create_temp_files):
        """Тест удаления ключа"""
        file1 = create_temp_files({"name": "John", "age": 30})
        file2 = create_temp_files({"name": "John"})

        result = generate_diff(file1, file2)

        expected = """{
  - age: 30
    name: John
}"""
        assert result == expected

    def test_boolean_values(self, create_temp_files):
        """Тест с булевыми значениями"""
        file1 = create_temp_files({"flag": True, "active": False})
        file2 = create_temp_files({"flag": False, "active": True})

        result = generate_diff(file1, file2)

        # Проверяем что форматирование булевых значений работает
        assert "false" in result
        assert "true" in result

    def test_none_values(self, create_temp_files):
        """Тест с None значениями"""
        file1 = create_temp_files({"value": None, "data": "test"})
        file2 = create_temp_files({"value": "not null", "data": "test"})

        result = generate_diff(file1, file2)

        # Проверяем что форматирование None работает
        assert "null" in result


# Быстрый тест для проверки импорта
def test_import():
    """Простой тест чтобы проверить что импорт работает"""
    assert callable(generate_diff)


@pytest.mark.parametrize("data1,data2,expected_contains", [
    # Добавление ключа
    ({"a": 1}, {"a": 1, "b": 2}, ["+ b: 2"]),
    # Удаление ключа
    ({"a": 1, "b": 2}, {"a": 1}, ["- b: 2"]),
    # Изменение значения
    ({"a": 1}, {"a": 2}, ["- a: 1", "+ a: 2"]),
    # Без изменений
    ({"a": 1}, {"a": 1}, ["a: 1"]),
])
def test_parametrized_scenarios(create_temp_files, data1, data2, expected_contains):
    """Параметризованные тесты для различных сценариев сравнения"""
    file1 = create_temp_files(data1)
    file2 = create_temp_files(data2)

    result = generate_diff(file1, file2)

    for expected_string in expected_contains:
        assert expected_string in result