import json
import os


class Loader:
    def __init__(self, directory):
        real_path = os.path.realpath(directory)
        if not os.path.exists(real_path):
            raise BadLoaderData
        self.directory = real_path

    def load_from_file(self, filename):
        path = os.path.join(self.directory, filename)
        if(os.path.realpath(path).startswith(self.directory)):
            handle = open(path, "r")
            blob = json.load(handle)
            return blob
        else:
            raise BadLoaderData

    def load_from_json(self, json_blob):
        try:
            data = json.loads(json_blob)
        except ValueError:
            data = self.load_from_file(json_blob)

        return self.load(data)

    def load(self, data):
        if(not isinstance(data, dict)):
            result = self.load_from_json(data)
        else:
            result = data

        return result


class BadLoaderData(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
