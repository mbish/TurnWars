from game.transport import Transport
from game.factories.factory import Factory
from game.serializable import Serializable
from game.exceptions import BadFactoryData


class TransportFactory(Factory):

    def __init__(self, factory_data, transport_class=Transport):
        Factory.__init__(self, factory_data, transport_class)
        return

    def validate_data(self, data):
        if('spaces_per_turn' not in data):
            raise BadFactoryData("spaces_per_turn not found")
        elif('cost_table' not in data):
            raise BadFactoryData("cost_table not found")
        else:
            return True

    def create(self, name):
        data = self.get_data(name)
        if('starting_fuel' in data):
            return self.creation_class(name, data['spaces_per_turn'],
                                       data['cost_table'],
                                       data['starting_fuel'])
        else:
            return self.creation_class(name, data['spaces_per_turn'],
                                       data['cost_table'])
