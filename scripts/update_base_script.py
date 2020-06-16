import json


def update_base(text: str):
    ret = ''
    json_string = json.loads(text)
    for chat_id, val in json_string.items():
        items = ''
        for i in range(len(val)):
            items += f'{{"title": "{val[i]}", "done": false}}'
            if i < len(val) - 1:
                items += ','
        ret += f'"{chat_id}": [{items}]'
    return '{' + ret + '}'


if __name__ == '__main__':
    with open('../data_base.json', 'r') as file:
        data = file.read()
    data = update_base(data)
    with open('../data_base.json', 'w') as file:
        file.write(data)
