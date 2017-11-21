import ujson


class JsonInputEvent:

    def __init__(self, method, timestamp, params):
        self.method = method
        self.timestamp = timestamp
        self.params = params

    @classmethod
    def from_dict(cls, dct):
        params = dict(dct)
        if all(key in dct for key in ('type', 'timestamp')):
            method = params.pop('type')
            timestamp = params.pop('timestamp')
        elif dct['type'] == 'Summary':
            method = params.pop('type')
            timestamp = params.pop('timestamp', None)
        else:
            raise ValueError('Incorrect event structure!')

        return cls(
            method=method,
            timestamp=timestamp,
            params=params,
        )

    @classmethod
    def from_json(cls, message):
        dct = ujson.loads(message)

        if not isinstance(dct, dict):
            raise ValueError('Received non-dict msg!')

        return cls.from_dict(dct)
