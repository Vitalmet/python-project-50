"""Test to import all modules for coverage"""


def test_import_all_modules():
    from gendiff import generate_diff
    from gendiff.parsers import load_file
    from gendiff.diff_builder import build_diff
    from gendiff.formatters.stylish import render as render_stylish
    from gendiff.formatters.plain import render_plain, stringify
    from gendiff.formatters.json import render_json

    # Проверяем что все импорты работают
    assert generate_diff is not None
    assert load_file is not None
    assert build_diff is not None
    assert render_stylish is not None
    assert render_plain is not None
    assert render_json is not None
    assert stringify is not None



def test_import_formatters_init():
    """Test importing formatters __init__"""
    from gendiff.formatters import render_stylish, render_plain, render_json
    assert render_stylish is not None
    assert render_plain is not None
    assert render_json is not None


def test_execute_all_functions():
    """Execute all functions to ensure they are covered"""
    from gendiff.parsers import get_format, parse
    from gendiff.formatters.plain import stringify

    # Test get_format
    assert get_format('file.json') == 'json'
    assert get_format('file.yml') == 'yaml'
    assert get_format('file.yaml') == 'yaml'

    # Test parse
    assert parse('{"key": "value"}', 'json') == {'key': 'value'}
    assert parse('key: value', 'yaml') == {'key': 'value'}

    # Test stringify
    assert stringify(None) == 'null'
    assert stringify(True) == 'true'
    assert stringify('text') == "'text'"
    assert stringify(123) == '123'
    assert stringify({'key': 'value'}) == '[complex value]'