import json


def render_json(diff):
    """
    Рендерит diff в формате JSON
    """

    def process_node(node):
        node_type = node['type']

        if node_type == 'nested':
            return {
                'type': 'nested',
                'children': {
                    key: process_node(child)
                    for key, child in node['children'].items()
                }
            }
        elif node_type == 'changed':
            return {
                'type': 'changed',
                'old_value': node['old_value'],
                'new_value': node['new_value']
            }
        else:
            result = {'type': node_type}
            if 'value' in node:
                result['value'] = node['value']
            return result

    processed_diff = {key: process_node(node) for key, node in diff.items()}
    return json.dumps(processed_diff, indent=2, ensure_ascii=False)