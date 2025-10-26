def test_import_all_modules():
    # Импортируем все основные модули
    from gendiff.gendiff import generate_diff
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
