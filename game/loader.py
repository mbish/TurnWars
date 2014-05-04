import json


class Loader:

    def load_from_file(self, filename):
        handle = open(filename, "r")
        blob = json.load(handle)
        return self.load_from_json(blob)

    def load_from_json(self, json_blob):
        try:
            data = json.loads(json_blob)
        except ValueError:
            data = self.load_from_file(json_blob)

        return self.load(data)

    def load(self, data):
        if(not isinstance(data, hash)):
            result = self.load_from_json(data)
        else:
            result = data

        return result


class BadLoaderData(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
