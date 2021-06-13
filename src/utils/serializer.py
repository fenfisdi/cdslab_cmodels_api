from json import JSONEncoder, loads


def encode_request(data: dict):
    raw = JSONEncoder().encode(data)
    return loads(raw)
