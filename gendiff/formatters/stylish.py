def stringify(value, depth):
    """
    Преобразует значение в строку с правильным форматированием
    """
    if value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, dict):
        return format_dict(value, depth + 1)
    else:
        return str(value)


def format_dict(dictionary, depth):
    """
    Форматирует словарь для вывода с правильными отступами
    """
    indent = '    ' * depth
    lines = []

    for key, value in sorted(dictionary.items()):
        formatted_value = stringify(value, depth)
        lines.append(f"{indent}{key}: {formatted_value}")

    result = ['{'] + lines + [f"{'    ' * (depth - 1)}" + '}']
    return '\n'.join(result)


def format_diff(diff, depth=0):
    """
    Форматирует diff в stylish формате
    """
    indent = '    ' * depth
    lines = []

    for key in sorted(diff.keys()):
        node = diff[key]
        node_type = node['type']

        if node_type == 'nested':
            children_formatted = format_diff(node['children'], depth + 1)
            lines.append(f"{indent}    {key}: {children_formatted}")
        elif node_type == 'added':
            value_formatted = stringify(node['value'], depth + 1)
            lines.append(f"{indent}  + {key}: {value_formatted}")
        elif node_type == 'removed':
            value_formatted = stringify(node['value'], depth + 1)
            lines.append(f"{indent}  - {key}: {value_formatted}")
        elif node_type == 'changed':
            old_value_formatted = stringify(node['old_value'], depth + 1)
            new_value_formatted = stringify(node['new_value'], depth + 1)
            lines.append(f"{indent}  - {key}: {old_value_formatted}")
            lines.append(f"{indent}  + {key}: {new_value_formatted}")
        elif node_type == 'unchanged':
            value_formatted = stringify(node['value'], depth + 1)
            lines.append(f"{indent}    {key}: {value_formatted}")

    if depth == 0:
        result = ['{'] + lines + ['}']
    else:
        result = ['{'] + lines + [f"{indent}" + '}']

    return '\n'.join(result)


def render(diff):
    """
    Рендерит diff в stylish формате
    """
    return format_diff(diff)