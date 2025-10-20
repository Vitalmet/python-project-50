import os
import json
import tempfile
import pytest
from gendiff import generate_diff


class TestSpecificFiles:
    """Тесты для конкретных файлов из задания"""

    @pytest.fixture
    def create_specific_files(self):
        """Фикстура для создания тестовых файлов из задания"""
        files = []

        def _create_file1():
            content = {
                "host": "hexlet.io",
                "timeout": 50,
                "proxy": "123.234.53.22",
                "follow": False
            }
            fd, path = tempfile.mkstemp(suffix='.json', dir=os.getcwd())
            with os.fdopen(fd, 'w') as f:
                json.dump(content, f)
            files.append(path)
            return path

        def _create_file2():
            content = {
                "timeout": 20,
                "verbose": True,
                "host": "hexlet.io"
            }
            fd, path = tempfile.mkstemp(suffix='.json', dir=os.getcwd())
            with os.fdopen(fd, 'w') as f:
                json.dump(content, f)
            files.append(path)
            return path

        yield _create_file1, _create_file2

        # Очистка
        for file_path in files:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_specific_files_comparison(self, create_specific_files):
        """Тест сравнения конкретных файлов из задания"""
        create_file1, create_file2 = create_specific_files
        file1 = create_file1()
        file2 = create_file2()

        result = generate_diff(file1, file2)

        # Ожидаемый результат для этих конкретных файлов
        expected = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
        assert result == expected

    def test_specific_files_structure(self, create_specific_files):
        """Тест структуры вывода для конкретных файлов"""
        create_file1, create_file2 = create_specific_files
        file1 = create_file1()
        file2 = create_file2()

        result = generate_diff(file1, file2)

        # Проверяем наличие конкретных строк в выводе
        assert "  - follow: false" in result
        assert "    host: hexlet.io" in result  # одинаковый ключ
        assert "  - proxy: 123.234.53.22" in result  # удаленный ключ
        assert "  - timeout: 50" in result
        assert "  + timeout: 20" in result  # измененный ключ
        assert "  + verbose: true" in result  # добавленный ключ

    def test_specific_files_analysis(self, create_specific_files):
        """Детальный анализ изменений в конкретных файлах"""
        create_file1, create_file2 = create_specific_files
        file1 = create_file1()
        file2 = create_file2()

        result = generate_diff(file1, file2)
        lines = result.strip().split('\n')

        # Анализируем какие изменения произошли
        removed_keys = [line for line in lines if line.startswith('  -')]
        added_keys = [line for line in lines if line.startswith('  +')]
        unchanged_keys = [line for line in lines if line.startswith('    ')]

        # Проверяем ожидаемые изменения
        assert len(removed_keys) == 3  # follow, proxy, timeout (старое значение)
        assert len(added_keys) == 2  # timeout (новое значение), verbose
        assert len(unchanged_keys) == 1  # host

        # Проверяем конкретные ключи
        assert any('follow: false' in line for line in removed_keys)
        assert any('proxy: 123.234.53.22' in line for line in removed_keys)
        assert any('timeout: 50' in line for line in removed_keys)
        assert any('timeout: 20' in line for line in added_keys)
        assert any('verbose: true' in line for line in added_keys)
        assert any('host: hexlet.io' in line for line in unchanged_keys)


def test_specific_files_content():
    """Тест который создает точно такие же файлы как в задании"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        json.dump({
            "host": "hexlet.io",
            "timeout": 50,
            "proxy": "123.234.53.22",
            "follow": False
        }, f1)
        file1_path = f1.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump({
            "timeout": 20,
            "verbose": True,
            "host": "hexlet.io"
        }, f2)
        file2_path = f2.name

    try:
        result = generate_diff(file1_path, file2_path)

        # Проверяем точное соответствие ожидаемому результату
        expected = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
        assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"

    finally:
        # Очистка
        os.unlink(file1_path)
        os.unlink(file2_path)


@pytest.mark.parametrize("file1_data,file2_data,expected_lines", [
    (
            # Ваши конкретные файлы
            {
                "host": "hexlet.io",
                "timeout": 50,
                "proxy": "123.234.53.22",
                "follow": False
            },
            {
                "timeout": 20,
                "verbose": True,
                "host": "hexlet.io"
            },
            [
                "  - follow: false",
                "    host: hexlet.io",
                "  - proxy: 123.234.53.22",
                "  - timeout: 50",
                "  + timeout: 20",
                "  + verbose: true"
            ]
    )
])
def test_parametrized_specific_files(file1_data, file2_data, expected_lines):
    """Параметризованный тест для конкретных файлов"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        json.dump(file1_data, f1)
        file1_path = f1.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(file2_data, f2)
        file2_path = f2.name

    try:
        result = generate_diff(file1_path, file2_path)

        # Проверяем что все ожидаемые строки присутствуют в результате
        for expected_line in expected_lines:
            assert expected_line in result, f"Expected line '{expected_line}' not found in result"

        assert result.startswith("{\n")
        assert result.endswith("\n}")

    finally:
        os.unlink(file1_path)
        os.unlink(file2_path)