import json
from gendiff.formatters.json import render_json


def test_json_formatter_basic():
    diff = {
        'key1': {'type': 'unchanged', 'value': 'value1'},
        'key2': {'type': 'added', 'value': 'value2'},
        'key3': {'type': 'removed', 'value': 'value3'},
    }

    result = render_json(diff)
    parsed_result = json.loads(result)

    assert isinstance(parsed_result, dict)
    assert 'key1' in parsed_result
    assert parsed_result['key1']['type'] == 'unchanged'
    assert parsed_result['key1']['value'] == 'value1'


def test_json_formatter_nested():
    diff = {
        'common': {
            'type': 'nested',
            'children': {
                'setting1': {'type': 'unchanged', 'value': 'Value 1'},
                'setting2': {'type': 'removed', 'value': 200},
            }
        }
    }

    result = render_json(diff)
    parsed_result = json.loads(result)

    assert parsed_result['common']['type'] == 'nested'
    assert isinstance(parsed_result['common']['children'], dict)
    assert 'setting1' in parsed_result['common']['children']


def test_json_formatter_changed():
    diff = {
        'key': {
            'type': 'changed',
            'old_value': 'old',
            'new_value': 'new'
        }
    }

    result = render_json(diff)
    parsed_result = json.loads(result)

    assert parsed_result['key']['type'] == 'changed'
    assert parsed_result['key']['old_value'] == 'old'
    assert parsed_result['key']['new_value'] == 'new'


def test_json_formatter_complex_values():
    diff = {
        'null_key': {'type': 'unchanged', 'value': None},
        'bool_key': {'type': 'unchanged', 'value': True},
        'number_key': {'type': 'unchanged', 'value': 42},
        'dict_key': {'type': 'unchanged', 'value': {'nested': 'value'}},
        'list_key': {'type': 'unchanged', 'value': [1, 2, 3]},
    }

    result = render_json(diff)
    parsed_result = json.loads(result)

    assert parsed_result['null_key']['value'] is None
    assert parsed_result['bool_key']['value'] is True
    assert parsed_result['number_key']['value'] == 42
    assert parsed_result['dict_key']['value'] == {'nested': 'value'}
    assert parsed_result['list_key']['value'] == [1, 2, 3]


def test_json_formatter_valid_json():
    diff = {
        'simple': {'type': 'unchanged', 'value': 'test'}
    }

    result = render_json(diff)
    assert json.loads(result) is not None
    assert isinstance(result, str)