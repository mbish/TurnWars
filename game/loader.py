import json


class Loader:

    def load_from_file(self, filename):
        handle = open(filename, "r")
        blob = json.load(handle)
        return self.load_from_json(blob)

    def load_from_json(self, json_blob):
        print json.loads(json_blob)
        return self.load(json.loads(json_blob))

    def load(self, data):
        if(self._validate_data(data)):
            return self._load_data(data)
        else:
            raise BadLoaderData("Could not load data {}".format(data))

    def _validate_data(self, data):
        raise NotImplementedError(
            "Loader class must implement validate_data(self, data)")

    def _load_data(self, data):
        raise NotImplementedError(
            "Loader class must implement validate_data(self, data)")


class BadLoaderData(Exception):
    def __init__(self, message):
        return Exception.__init__(self, message)
