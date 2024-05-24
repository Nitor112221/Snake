import json


def get_statistic():
    with open("data/statistic.json", 'r') as file:
        json_file = json.load(file)
        return json_file['max_apple']


def save_statistic(**kwargs):
    mx_apple = get_statistic()
    kwargs["max_apple"] = max(kwargs["max_apple"], mx_apple)
    dict_json = kwargs
    with open("data/statistic.json", 'w') as file:
        json.dump(dict_json, file)
