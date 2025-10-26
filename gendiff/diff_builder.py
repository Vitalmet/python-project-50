def build_diff(data1, data2):
    """
    Строит внутреннее представление различий между двумя структурами
    """
    diff = {}
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))

    for key in all_keys:
        value1 = data1.get(key)
        value2 = data2.get(key)

        if key not in data1:
            # Ключ добавлен во втором файле
            diff[key] = {
                'type': 'added',
                'value': value2
            }
        elif key not in data2:
            # Ключ удален из первого файла
            diff[key] = {
                'type': 'removed',
                'value': value1
            }
        elif isinstance(value1, dict) and isinstance(value2, dict):
            # Оба значения - словари, рекурсивно строим diff
            diff[key] = {
                'type': 'nested',
                'children': build_diff(value1, value2)
            }
        elif value1 == value2:
            # Значения одинаковые - показываем без изменений
            diff[key] = {
                'type': 'unchanged',
                'value': value1
            }
        else:
            # Значения разные
            diff[key] = {
                'type': 'changed',
                'old_value': value1,
                'new_value': value2
            }

    return diff
