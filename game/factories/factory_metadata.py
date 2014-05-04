

class FactoryMetadata:
    def __init__(self, factory_class, creation_class, dependencies, data):
        self.creation_class = creation_class
        self.dependencies = dependencies
        self.data = data
        self.factory_class = factory_class

    def get_creation_class(self):
        return self.creation_class

    def get_dependencies(self):
        return self.dependencies

    def get_data(self):
        return self.data

    def get_factory_class(self):
        return self.factory_class
