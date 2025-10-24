import pytest
import os
import tempfile
import subprocess
import sys
from gendiff.scripts.gendiff import main


def test_main_with_valid_files(capsys):
    """Тест main с валидными файлами"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    # Сохраняем оригинальные sys.argv
    original_argv = sys.argv

    try:
        # Устанавливаем тестовые аргументы
        sys.argv = ['gendiff', file1, file2]

        # Запускаем main
        main()

        # Перехватываем вывод
        captured = capsys.readouterr()
        output = captured.out

        # Проверяем что вывод содержит ожидаемые данные
        assert 'common' in output
        assert 'follow' in output
        assert len(output) > 0

    finally:
        # Восстанавливаем оригинальные аргументы
        sys.argv = original_argv


def test_main_with_format_option(capsys):
    """Тест main с опцией формата"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    original_argv = sys.argv

    try:
        sys.argv = ['gendiff', file1, file2, '--format', 'stylish']
        main()

        captured = capsys.readouterr()
        output = captured.out

        assert 'common' in output
        assert len(output) > 0

    finally:
        sys.argv = original_argv


def test_main_with_help_option(capsys):
    """Тест main с опцией помощи"""
    original_argv = sys.argv

    try:
        sys.argv = ['gendiff', '--help']

        with pytest.raises(SystemExit) as exc_info:
            main()

        # --help должен вызвать SystemExit(0)
        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        output = captured.out

        assert 'Compares two configuration files' in output
        assert '--format' in output

    finally:
        sys.argv = original_argv


def test_main_with_version_option(capsys):
    """Тест main с опцией версии"""
    original_argv = sys.argv

    try:
        sys.argv = ['gendiff', '--version']

        with pytest.raises(SystemExit) as exc_info:
            main()

        captured = capsys.readouterr()
        output = captured.out

        assert 'gendiff 1.0' in output

    finally:
        sys.argv = original_argv


def test_main_with_nonexistent_file(capsys):
    """Тест main с несуществующим файлом"""
    original_argv = sys.argv

    try:
        sys.argv = ['gendiff', 'nonexistent1.json', 'nonexistent2.json']

        result = main()

        # Должен вернуть код ошибки 1
        assert result == 1

        captured = capsys.readouterr()
        output = captured.out

        assert "not found" in output

    finally:
        sys.argv = original_argv


def test_main_with_missing_arguments(capsys):
    """Тест main с недостающими аргументами"""
    original_argv = sys.argv

    try:
        sys.argv = ['gendiff']  # Нет аргументов

        # Ожидаем SystemExit с кодом 2 (ошибка аргументов)
        with pytest.raises(SystemExit) as exc_info:
            main()

        # Код ошибки должен быть 2
        assert exc_info.value.code == 2

        captured = capsys.readouterr()
        error_output = captured.err

        # Проверяем сообщение об ошибке
        assert 'error:' in error_output
        assert 'required' in error_output

    finally:
        sys.argv = original_argv