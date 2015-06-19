class Builder:
    def __init__(self, creation_class):
        self.creation_class = creation_class
        self._instance = creation_class()

    def pop_instance(self):
        try:
            self._instance.validate()
        except Exception as e:
            raise BuildInvalid()

        instance = self._instance
        self._instance = self.creation_class()
        return instance


class BuildInvalid(Exception):
    def __init__(self, message=''):
        super(BuildInvalid, self).__init__(message)

