import ujson


class JsonOutputEvent:

    def __init__(self, method, **params):
        self.method = method
        self.params = params

    def to_dict(self):
        dct = dict(self.params)
        dct['method'] = self.method
        return dct

    def to_json(self):
        dct = self.to_dict()
        return ujson.dumps(dct)
