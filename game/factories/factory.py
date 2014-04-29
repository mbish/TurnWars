from game.serializable import Serializable


class Factory(Serializable):

    def __init__(self, factory_data, creation_class):
        for data in factory_data:
            if(not self.validate_data(factory_data[data])):
                raise BadFactoryData("Data for {0} is malformed".format(data))

        self.creation_class = creation_class
        self.factory_data = factory_data
        return

    def validate_data(self, key):
        raise NotImplementedError(
            "Factory class must implement validate_data(self, data)")

    def create(self, name):
        raise NotImplementedError(
            "Factory class must implement create(self, name)")

    def can_make(self, name):
        return (name in self.factory_data)

    def get_data(self, name):
        if(name not in self.factory_data):
            raise BadFactoryRequest(
                "Cannot find factory data for {0}".format(name))
        return self.factory_data[name]

    def flat(self):
        return self.factory_data


class BadFactoryData(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


class BadFactoryRequest(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
