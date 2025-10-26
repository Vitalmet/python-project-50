import os
import tempfile
import pytest
from unittest.mock import patch


def test_main_file1_not_found():
    from gendiff.__main__ import main

    with patch('sys.argv', ['gendiff', 'nonexistent1.json', 'tests/fixtures/file1.json']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1


def test_main_file2_not_found():
    from gendiff.__main__ import main

    with patch('sys.argv', ['gendiff', 'tests/fixtures/file1.json', 'nonexistent2.json']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1


def test_main_unexpected_error():
    from gendiff.__main__ import main

    # Mock generate_diff to raise an unexpected exception
    with patch('gendiff.__main__.generate_diff') as mock_generate:
        mock_generate.side_effect = Exception("Unexpected error")

        with patch('sys.argv', ['gendiff', 'tests/fixtures/file1.json', 'tests/fixtures/file2.json']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1


def test_gendiff_unsupported_format():
    from gendiff.gendiff import generate_diff

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        f1.write('{"key": "value"}')
        file1 = f1.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        f2.write('{"key": "value"}')
        file2 = f2.name

    try:
        with pytest.raises(ValueError, match="Unsupported format"):
            generate_diff(file1, file2, 'invalid_format')
    finally:
        os.unlink(file1)
        os.unlink(file2)


def test_main_invalid_format():
    from gendiff.__main__ import main

    with patch('sys.argv', ['gendiff', 'tests/fixtures/file1.json', 'tests/fixtures/file2.json', '-f', 'invalid']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 2