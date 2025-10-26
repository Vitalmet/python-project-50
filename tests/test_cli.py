import pytest
import os
import sys
from gendiff.__main__ import main


def test_main_with_valid_files(capsys):
    """Тест main с валидными файлами"""
    file1 = os.path.join('tests', 'fixtures', 'file1.json')
    file2 = os.path.join('tests', 'fixtures', 'file2.json')

    original_argv = sys.argv

    try:
        sys.argv = ['gendiff', file1, file2]
        main()

        captured = capsys.readouterr()
        output = captured.out

        assert 'common' in output
        assert 'follow' in output
        assert len(output) > 0

    finally:
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

        with pytest.raises(SystemExit):
            main()

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

        with pytest.raises(SystemExit):
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
    except SystemExit as e:
        # Ловим SystemExit и проверяем stderr
        captured = capsys.readouterr()
        assert 'not found' in captured.err
        assert e.code == 1
    else:
        assert False, "Expected SystemExit"
    finally:
        sys.argv = original_argv


def test_main_with_missing_arguments(capsys):
    """Тест main с недостающими аргументами"""
    original_argv = sys.argv

    try:
        sys.argv = ['gendiff']

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 2

        captured = capsys.readouterr()
        error_output = captured.err

        assert 'error:' in error_output
        assert 'required' in error_output

    finally:
        sys.argv = original_argv