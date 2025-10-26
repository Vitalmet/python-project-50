import os
from gendiff.formatters.plain import render_plain, stringify
from gendiff.gendiff import generate_diff


def test_stringify():
    """Тест функции stringify"""
    assert stringify("value") == "'value'"
    assert stringify(42) == "42"
    assert stringify(True) == "true"
    assert stringify(False) == "false"
    assert stringify(None) == "null"
    assert stringify({"key": "value"}) == "[complex value]"
    assert stringify([1, 2, 3]) == "[complex value]"


def test_render_plain_simple():
    """Тест простого plain формата"""
    diff = {
        "key1": {"type": "added", "value": "value1"},
        "key2": {"type": "removed", "value": "value2"},
        "key3": {"type": "changed", "old_value": "old", "new_value": "new"},
        "key4": {"type": "unchanged", "value": "same"},  # должен игнорироваться
    }

    result = render_plain(diff)
    expected_lines = [
        "Property 'key1' was added with value: 'value1'",
        "Property 'key2' was removed",
        "Property 'key3' was updated. From 'old' to 'new'",
    ]

    for line in expected_lines:
        assert line in result

    # unchanged не должен отображаться
    assert "Property 'key4'" not in result


def test_render_plain_nested():
    """Тест plain формата с вложенными структурами"""
    diff = {
        "common": {
            "type": "nested",
            "children": {
                "follow": {"type": "added", "value": False},
                "setting1": {"type": "unchanged", "value": "Value 1"},
            },
        }
    }

    result = render_plain(diff)
    assert "Property 'common.follow' was added with value: false" in result
    # unchanged не должен отображаться
    assert "Property 'common.setting1'" not in result


def test_render_plain_complex_values():
    """Тест plain формата со сложными значениями"""
    diff = {"setting": {"type": "added", "value": {"nested": "value"}}}

    result = render_plain(diff)
    assert "Property 'setting' was added with value: [complex value]" in result


def test_generate_diff_with_plain_format():
    """Интеграционный тест generate_diff с plain форматом"""
    file1 = os.path.join("tests", "fixtures", "file1.json")
    file2 = os.path.join("tests", "fixtures", "file2.json")

    result = generate_diff(file1, file2, "plain")

    assert isinstance(result, str)
    # Проверяем специфичные для plain формата паттерны
    assert any(word in result for word in ["added", "removed", "updated"])


def test_render_plain_empty():
    """Тест plain формата с пустым diff"""
    result = render_plain({})
    assert result == ""


def test_cli_with_plain_format():
    """Тест CLI с plain форматом"""
    file1 = os.path.join("tests", "fixtures", "file1.json")
    file2 = os.path.join("tests", "fixtures", "file2.json")

    result = generate_diff(file1, file2, "plain")
    assert isinstance(result, str)
