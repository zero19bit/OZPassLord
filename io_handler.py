import csv
import json


def export_to_csv(passwords, filepath):
    keys = passwords[0].keys() if passwords else []
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(passwords)
    return "done"




def export_to_json(passwords, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(passwords, f, indent=4, ensure_ascii=False)
    return "done"




def import_from_csv(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)



def import_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)



def detect_format(filepath):
    if filepath.endswith('.csv'):
        return 'csv'
    elif filepath.endswith('.json'):
        return 'json'
    else:
        raise ValueError("Unsupported file format")