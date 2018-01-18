from game.transport import Transport
from game.exceptions import BadTransportRequest, BadTransportCreation
from nose.tools import assert_raises


def bad_constructor_test():
    assert_raises(BadTransportCreation, Transport, 'tred', -1, 20)


def move_test():
    transport = Transport('tred', 10, {}, 20)
    assert transport.get_spaces_left() == 10
    transport.move(5)
    assert transport.get_spaces_left() == 5
    transport.move(5)
    assert transport.get_spaces_left() == 0
    assert_raises(BadTransportRequest, transport.move, 5)


def fuel_test():
    transport = Transport('tred', 30, {}, 10)
    assert transport.get_spaces_left() == 10
    assert_raises(BadTransportRequest, transport.move, 20)
    transport.refuel()
    assert transport.get_spaces_left() == 10
    transport.move(10)
    assert transport.get_spaces_left() == 0
    transport.refuel()
    assert_raises(BadTransportRequest, transport.use_fuel, 11)


def non_fuel_test():
    transport = Transport('foot', 10, {})
    assert not transport.uses_fuel()
    assert transport.get_spaces_left() == 10
    transport.move(5)
    assert transport.get_spaces_left() == 5
    transport.refuel()
    assert transport.get_spaces_left() == 5
    transport.reset()
    assert transport.get_spaces_left() == 10


def serialize_test():
    transport = Transport('pogo-stick', 2, {})
    json_string = ('{"fuel": -1, "hasMoved": false, "name": "pogo-stick", "spaces_left": 2}')
    print(transport.as_json())
    assert transport.as_json() == json_string
