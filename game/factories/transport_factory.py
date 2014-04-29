from game.transport import Transport
from game.factories.factory import Factory
from game.serializable import Serializable


class TransportFactory(Factory):

    def __init__(self, factory_data, transport_class=Transport):
        Factory.__init__(self, factory_data, transport_class)
        return

    def validate_data(self, data):
        if('spaces_per_turn' not in data):
            return False
        else:
            return True

    def create(self, name):
        data = self.get_data(name)
        if('starting_fuel' in data):
            return self.creation_class(name, data['spaces_per_turn'],
                                       data['starting_fuel'])
        else:
            return self.creation_class(name, data['spaces_per_turn'])
