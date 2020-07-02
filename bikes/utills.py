def query_value_serialize(key, value):
    if key.endswith('__in') or key.endswith('__in[]'):
        return [query_value_serialize('', [i]) for i in value]

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

def key_serialize(key):
    if key.endswith('[]'):
        return key[:-len('[]')]
    else:
        return key

def serialize_query_params(query_params):
    query_params = {
        key_serialize(key): query_value_serialize(key, query_params.getlist(key))
        for key in query_params.keys()
    }

    return query_params
    