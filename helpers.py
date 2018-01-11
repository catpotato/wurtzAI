import csv

def get_csv_as_dict(path):
    reader = csv.reader(open(path, 'r'))
    d = {}
    for row in reader:
        k, v = row
        d[k] = v

    return d

def get_csv_as_list_dict(path):
    reader = csv.reader(open(path, 'r'))
    next(reader, None)  # skip the headers
    l = []
    for row in reader:
        k, v = row
        l.append({'question':k, 'answer':v})

    return l

def merge_dictionaries(list_of_dicts):
    result = {}
    for d in list_of_dicts:
        result.update(d)
    return result

def merge_keys_and_values(d):
    keys = []
    values = []

    for key, value in d.values:
        keys.append(key)
        values.append(value)

    return (''.join(keys), ''.join(values))
