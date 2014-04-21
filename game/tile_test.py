from tile import Tile


def serialize_test():
    tile = Tile("foo", 4, {}, {})
    assert tile.as_json() == '"foo"'
