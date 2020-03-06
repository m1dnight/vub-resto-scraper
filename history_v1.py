import json

import json
import os

FILENAMES = ["jette.en.json", "jette.nl.json", "etterbeek.en.json", "etterbeek.nl.json"]


def history(directory, history):
    for filename in FILENAMES:
        latest_path = os.path.join(directory, filename)
        history_path = os.path.join(history, filename)

        latest_content = read_file_to_json(latest_path)
        history_content = read_file_to_json(history_path)

        for day in latest_content:
            key = day["date"]
            val = day["menus"]
            history_content[key] = val

        write_json_to_file(history_path, history_content)


def read_file_to_json(file):
    if not os.path.exists(file):
        return {}
    else:
        with open(file) as f:
            content = json.load(f)
            return content


def write_json_to_file(file, json_dict):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=2)
