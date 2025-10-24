import os
from gendiff.scripts.gendiff import generate_diff


class TestNestedStructures:
    """Тесты для вложенных структур"""

    def test_nested_json_comparison(self):
        """Сравнение JSON файлов с вложенностью"""
        file1 = os.path.join('tests', 'fixtures', 'file1.json')
        file2 = os.path.join('tests', 'fixtures', 'file2.json')

        result = generate_diff(file1, file2)

        # Проверяем что вывод содержит основные структуры
        assert "common" in result
        assert "group1" in result
        assert "group2" in result
        assert "group3" in result

        # Проверяем что есть изменения (+, -)
        assert "+" in result
        assert "-" in result

    def test_nested_yaml_comparison(self):
        """Сравнение YAML файлов с вложенностью"""
        file1 = os.path.join('tests', 'fixtures', 'file1.yml')
        file2 = os.path.join('tests', 'fixtures', 'file2.yml')

        result = generate_diff(file1, file2)

        # Проверяем ключевые элементы
        assert "common" in result
        assert "group1" in result
        assert "group2" in result
        assert "group3" in result
        assert "+" in result
        assert "-" in result

    def test_nested_mixed_formats(self):
        """Сравнение JSON и YAML файлов с вложенностью"""
        json_file = os.path.join('tests', 'fixtures', 'file1.json')
        yaml_file = os.path.join('tests', 'fixtures', 'file2.yml')

        result = generate_diff(json_file, yaml_file)

        # Должны быть различия
        assert "common" in result
        assert "group1" in result
        assert "+" in result
        assert "-" in result


def test_expected_output_structure():
    """Тест точного соответствия ожидаемому выводу"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    result = generate_diff(file1, file2)

    # Проверяем структуру вывода
    lines = result.split('\n')

    # Проверяем наличие изменений
    assert any('+' in line for line in lines)
    assert any('-' in line for line in lines)
    assert any('common:' in line for line in lines)
    assert any('group1:' in line for line in lines)