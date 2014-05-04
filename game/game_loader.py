from game.factories.factory_metadata import FactoryMetadata


class GameLoader:
    def __init__(self, metadata_class=FactoryMetadata):
        self.metadata_class = metadata_class
        self.metadata = {}
        self.factories = {}

    def set_metadata(self, name, factory_class,
                     creation_class, dependencies, data):
        self.metadata[name] = self.metadata_class(factory_class,
                                                  creation_class,
                                                  dependencies, data)

    def _build_factory(self, name):
        if(name not in self.metadata):
            raise BadGameLoaderRequest(
                "Cannot construct factory for {0}".format(name))
        if(name not in self.factories):
            metadata = self.metadata[name]
            built_dependencies = {}
            factory_dependencies = metadata.get_dependencies()
            for dependency in factory_dependencies:
                print "Got dependency {0}".format(dependency)
                built_dependencies[dependency] = (
                    self._build_factory(factory_dependencies[dependency]))

            built_dependencies['data'] = metadata.get_data()
            built_dependencies['creation_class'] = (
                metadata.get_creation_class())
            self.factories[name] = metadata.get_factory_class()(
                **built_dependencies)

        return self.factories[name]


class BadGameLoaderRequest(Exception):
    def __init__(self, message):
            Exception.__init__(self, message)
