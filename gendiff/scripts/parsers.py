import json
import yaml


def get_format(file_path):
    if file_path.endswith('.json'):
        return 'json'
    elif file_path.endswith(('.yml', '.yaml')):
        return 'yaml'
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


def parse(data, format_name):
    """Парсит данные в зависимости от формата"""
    if format_name == 'json':
        return json.loads(data)
    elif format_name == 'yaml':
        return yaml.safe_load(data)
    else:
        raise ValueError(f"Unsupported format: {format_name}")


def load_file(file_path):
    """Загружает и парсит файл"""
    with open(file_path, 'r') as f:
        content = f.read()

    file_format = get_format(file_path)
    return parse(content, file_format)