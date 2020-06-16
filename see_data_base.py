import json

try:
    data_base_file_name = 'data_base.json'
    with open(data_base_file_name, 'r') as file:
        data = file.read()
    data_base = json.loads(data)

    for key, val in data_base.items():
        print(key, val)
except FileNotFoundError as e:
    print('База не найдена')
    exit(0)