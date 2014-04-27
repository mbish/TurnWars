import json


class Loader:

    def load_from_file(self, filename):
        handle = open(filename, "r")
        blob = json.load(handle)
        return self.load_from_json(blob)

    def load_from_json(self, json_blob):
        return self.load(json.loads(json_blob))

    def load(self, data):
        return data


class BadLoaderData(Exception):
    def __init__(self, message):
        return Exception.__init__(self, message)
