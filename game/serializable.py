import json


class Serializable(object):
    def flat(self):
        raise NotImplementedError(
            "Serializable class must implement flat(self)")

    def as_json(self):
        return json.dumps(self.flat())
