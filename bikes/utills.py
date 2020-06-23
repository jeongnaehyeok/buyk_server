def serialize_query_params(query_params):
    query_params = {
        key_serialize(key): query_value_serialize(key, query_params.getlist(key))
        for key
        in query_params.keys()
    }

    return query_params