def stringify(value):
    """
    Преобразует значение в строку для plain формата
    """
    if isinstance(value, (dict, list)):
        return '[complex value]'
    elif value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, str):
        return f"'{value}'"
    else:
        return str(value)


def build_plain_lines(diff, path=''):
    lines = []

    for key in sorted(diff.keys()):
        node = diff[key]
        current_path = f"{path}.{key}" if path else key
        node_type = node['type']

        if node_type == 'nested':
            nested_lines = build_plain_lines(node['children'], current_path)
            lines.extend(nested_lines)
        elif node_type == 'added':
            value = stringify(node['value'])
            message = f"Property '{current_path}' was added with value: {value}"
            lines.append(message)
        elif node_type == 'removed':
            lines.append(f"Property '{current_path}' was removed")
        elif node_type == 'changed':
            old_value = stringify(node['old_value'])
            new_value = stringify(node['new_value'])
            message = (
                f"Property '{current_path}' was updated. "
                f"From {old_value} to {new_value}"
            )
            lines.append(message)

    return lines


def render_plain(diff):
    """
    Рендерит diff в plain формате
    """
    lines = build_plain_lines(diff)
    return '\n'.join(lines)
