import json


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value

def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value

def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        found = int(found[0])
    else:
        found = default
    return default

def print_range(flavor_list):
    for i, flavor in enumerate(flavor_list):
        print('{}, {}'.format(i+1, flavor))


def longest_name(names):
    letters = (len(x) for x in names)
    longest_name = None
    max_letters = 0
    for name, count in zip(names, letters):
        if count > max_letters:
            longest_name = name
            max_letters = count

UNDEFINED = object()
def divide_json(path):
    handle = open(path, 'r+')
    try:
        data = handle.read()
        op = json.loads(data)
        value = (op['numerator'] / op['denominator'])

    except ZeroDivisionError as e:
        return UNDEFINED

    else:
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)
        handle.write(result)
        return value
        
    finally:
        handle.close()



