def build_diff(data1, data2):
    diff = {}
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))

    for key in all_keys:
        vaulue1 = data1.get(key)
        vaulue2 = data2.get(key)

        if key not in data1:
            diff[key] = {
                'type': 'added',
                'value': vaulue2,
            }
        elif key not in data2:
            diff[key] = {
                'type': 'removed',
                'value': vaulue1,
            }
        elif isinstance(vaulue1, dict) and isinstance(vaulue2, dict):
            diff[key] = {
                'type': 'unchanged',
                'value': vaulue1,
            }
        else:
            diff[key] = {
                'type': 'changed',
                'old_value': vaulue1,
                'new_value': vaulue2,
            }
    return diff