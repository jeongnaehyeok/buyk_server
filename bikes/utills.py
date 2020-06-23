def query_value_serialize(key, value):
    try:
        value = value[-1]
    except IndexError:
        return None

    if value.isnumeric():
        return int(value)
    elif value == 'true':
        return True
    elif value == 'false':
        return False
    else:
        return value